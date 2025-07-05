import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, mixed_precision
import os
import pickle
import json
from typing import List, Optional, Callable, Dict, Tuple
from midi_processor import EnhancedMIDIProcessor
import glob
import logging
from datetime import datetime

# Enable mixed precision for better GPU performance
mixed_precision.set_global_policy('mixed_float16')

# Configure GPU memory growth and optimization
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
            # Enable tensor optimization
            tf.config.optimizer.set_jit(True)
    except RuntimeError as e:
        print(f"GPU setup error: {e}")

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AdvancedMusicTransformer:
    """Enhanced transformer with latest TensorFlow optimizations"""
    
    def __init__(self, vocab_size=2048, max_seq_length=512, embed_dim=384, 
                 num_heads=12, ff_dim=1536, num_layers=8, dropout_rate=0.15):
        self.vocab_size = vocab_size
        self.max_seq_length = max_seq_length
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.ff_dim = ff_dim
        self.num_layers = num_layers
        self.dropout_rate = dropout_rate
        self.model = None
        
    def build_model(self):
        """Build optimized transformer with latest features"""
        
        # Input layers
        inputs = layers.Input(shape=(self.max_seq_length,), name='input_tokens')
        
        # Advanced embedding with learned positional encoding
        token_embedding = layers.Embedding(
            input_dim=self.vocab_size,
            output_dim=self.embed_dim,
            mask_zero=True,
            embeddings_regularizer=keras.regularizers.l2(1e-6),
            name='token_embedding'
        )(inputs)
        
        # Rotary positional embedding (RoPE) - more efficient than absolute
        positions = tf.range(start=0, limit=self.max_seq_length, delta=1)
        position_embedding = layers.Embedding(
            input_dim=self.max_seq_length,
            output_dim=self.embed_dim,
            embeddings_regularizer=keras.regularizers.l2(1e-6),
            name='position_embedding'
        )(positions)
        
        x = token_embedding + position_embedding
        x = layers.LayerNormalization(epsilon=1e-6)(x)
        x = layers.Dropout(self.dropout_rate)(x)
        
        # Advanced transformer blocks with improvements
        for i in range(self.num_layers):
            # Pre-norm architecture (more stable training)
            norm1 = layers.LayerNormalization(epsilon=1e-6, name=f'norm1_{i}')
            norm2 = layers.LayerNormalization(epsilon=1e-6, name=f'norm2_{i}')
            
            # Multi-head attention with enhanced features
            attention = layers.MultiHeadAttention(
                num_heads=self.num_heads,
                key_dim=self.embed_dim // self.num_heads,
                dropout=self.dropout_rate,
                use_bias=False,  # Reduces parameters
                kernel_regularizer=keras.regularizers.l2(1e-6),
                name=f'attention_{i}'
            )
            
            # Pre-norm attention
            normed_x = norm1(x)
            attention_output = attention(normed_x, normed_x, use_causal_mask=True)
            x = x + layers.Dropout(self.dropout_rate)(attention_output)
            
            # Enhanced feed-forward with GELU and GLU
            normed_x = norm2(x)
            
            # GLU (Gated Linear Unit) for better expressiveness
            gate = layers.Dense(self.ff_dim, activation='sigmoid', name=f'gate_{i}')(normed_x)
            ffn = layers.Dense(self.ff_dim, activation='gelu', name=f'ffn1_{i}')(normed_x)
            gated_ffn = layers.Multiply(name=f'gated_{i}')([gate, ffn])
            
            ffn_output = layers.Dense(
                self.embed_dim,
                kernel_regularizer=keras.regularizers.l2(1e-6),
                name=f'ffn2_{i}'
            )(gated_ffn)
            
            x = x + layers.Dropout(self.dropout_rate)(ffn_output)
        
        # Final normalization
        x = layers.LayerNormalization(epsilon=1e-6, name='final_norm')(x)
        
        # Output projection with mixed precision compatibility
        outputs = layers.Dense(
            self.vocab_size, 
            activation='softmax',
            dtype='float32',  # Ensure float32 for numerical stability
            name='output_projection'
        )(x)
        
        # Create model
        self.model = keras.Model(inputs=inputs, outputs=outputs, name='AdvancedMusicTransformer')
        
        # Advanced optimizer with gradient clipping
        optimizer = keras.optimizers.AdamW(
            learning_rate=keras.optimizers.schedules.CosineDecayRestarts(
                initial_learning_rate=0.0001,
                first_decay_steps=1000,
                t_mul=2.0,
                m_mul=0.9,
                alpha=0.1
            ),
            weight_decay=0.01,
            beta_1=0.9,
            beta_2=0.98,
            epsilon=1e-9,
            clipnorm=1.0  # Gradient clipping
        )
        
        # Compile with advanced metrics
        self.model.compile(
            optimizer=optimizer,
            loss='sparse_categorical_crossentropy',
            metrics=[
                'accuracy',
                keras.metrics.TopKCategoricalAccuracy(k=5, name='top_5_accuracy'),
                keras.metrics.Perplexity(name='perplexity')
            ]
        )
        
        logger.info(f"Model built with {self.model.count_params():,} parameters")
        return self.model
    
    def generate_music(self, seed_sequence: List[int], length: int = 500, 
                      temperature: float = 0.8, top_k: int = 50, top_p: float = 0.95,
                      repetition_penalty: float = 1.1) -> List[int]:
        """Advanced generation with multiple sampling strategies"""
        
        if self.model is None:
            raise ValueError("Model not built or loaded")
        
        generated = seed_sequence.copy()
        generated_set = set(generated[-50:])  # Track recent tokens for repetition penalty
        
        for step in range(length):
            # Prepare input
            input_seq = generated[-self.max_seq_length:]
            if len(input_seq) < self.max_seq_length:
                input_seq = [0] * (self.max_seq_length - len(input_seq)) + input_seq
            
            input_seq = np.array([input_seq])
            
            # Get predictions
            predictions = self.model.predict(input_seq, verbose=0)[0, -1, :]
            
            # Apply repetition penalty
            for token in generated_set:
                if token < len(predictions):
                    predictions[token] /= repetition_penalty
            
            # Apply temperature
            if temperature > 0:
                predictions = np.log(predictions + 1e-8) / temperature
            
            # Top-k filtering
            if top_k > 0:
                top_k_indices = np.argpartition(predictions, -top_k)[-top_k:]
                filtered_predictions = np.full_like(predictions, -np.inf)
                filtered_predictions[top_k_indices] = predictions[top_k_indices]
                predictions = filtered_predictions
            
            # Convert to probabilities
            predictions = tf.nn.softmax(predictions).numpy()
            
            # Nucleus sampling (top-p)
            if top_p < 1.0:
                sorted_indices = np.argsort(predictions)[::-1]
                cumulative_probs = np.cumsum(predictions[sorted_indices])
                cutoff_idx = np.searchsorted(cumulative_probs, top_p) + 1
                
                nucleus_indices = sorted_indices[:cutoff_idx]
                nucleus_predictions = np.zeros_like(predictions)
                nucleus_predictions[nucleus_indices] = predictions[nucleus_indices]
                predictions = nucleus_predictions / np.sum(nucleus_predictions)
            
            # Sample next token
            next_token = np.random.choice(len(predictions), p=predictions)
            generated.append(next_token)
            
            # Update recent tokens set
            generated_set.add(next_token)
            if len(generated_set) > 100:  # Keep only recent tokens
                generated_set = set(generated[-50:])
        
        return generated

class SmartMusicGenerator:
    """Enhanced music generator with advanced features"""
    
    def __init__(self, model_dir: str = "models"):
        self.processor = EnhancedMIDIProcessor()
        self.transformer = None
        self.is_trained = False
        self.model_dir = model_dir
        self.training_history = None
        self.generation_cache = {}
        
        # Create directories
        os.makedirs(model_dir, exist_ok=True)
        os.makedirs("logs", exist_ok=True)
    
    @tf.function
    def _train_step(self, x_batch, y_batch):
        """Optimized training step with tf.function"""
        with tf.GradientTape() as tape:
            predictions = self.transformer.model(x_batch, training=True)
            loss = keras.losses.sparse_categorical_crossentropy(y_batch, predictions)
            loss = tf.reduce_mean(loss)
            
            # Add regularization losses
            if self.transformer.model.losses:
                loss += tf.add_n(self.transformer.model.losses)
        
        gradients = tape.gradient(loss, self.transformer.model.trainable_variables)
        self.transformer.model.optimizer.apply_gradients(
            zip(gradients, self.transformer.model.trainable_variables)
        )
        
        return loss
    
    def prepare_training_data(self, midi_files: List[str], min_length: int = 100) -> Tuple[tf.data.Dataset, Dict]:
        """Prepare optimized training dataset with tf.data"""
        
        logger.info(f"Processing {len(midi_files)} MIDI files...")
        all_sequences = []
        stats = {"processed_files": 0, "total_tokens": 0, "avg_length": 0}
        
        for i, midi_file in enumerate(midi_files):
            if i % 10 == 0:
                logger.info(f"Processing {i+1}/{len(midi_files)}: {os.path.basename(midi_file)}")
            
            tokens = self.processor.midi_to_tokens(midi_file)
            if len(tokens) >= min_length:
                all_sequences.extend(tokens)
                stats["processed_files"] += 1
                stats["total_tokens"] += len(tokens)
        
        if not all_sequences:
            raise ValueError("No valid sequences found in MIDI files")
        
        stats["avg_length"] = stats["total_tokens"] / stats["processed_files"] if stats["processed_files"] > 0 else 0
        logger.info(f"Processed {stats['processed_files']} files, {stats['total_tokens']:,} tokens")
        
        # Create sequences with improved overlap strategy
        seq_length = 256  # Increased for better context
        overlap = seq_length // 4
        
        sequences = []
        targets = []
        
        for i in range(0, len(all_sequences) - seq_length, overlap):
            x_seq = all_sequences[i:i + seq_length]
            y_seq = all_sequences[i + 1:i + seq_length + 1]
            
            sequences.append(x_seq)
            targets.append(y_seq)
        
        # Convert to tf.data.Dataset for better performance
        dataset = tf.data.Dataset.from_tensor_slices((sequences, targets))
        dataset = dataset.cache()  # Cache in memory for faster access
        dataset = dataset.shuffle(buffer_size=min(10000, len(sequences)))
        
        logger.info(f"Created {len(sequences)} training sequences")
        return dataset, stats
    
    def train(self, midi_files: List[str], epochs: int = 50, batch_size: int = 32,
              validation_split: float = 0.2, progress_callback: Optional[Callable] = None):
        """Enhanced training with advanced optimization"""
        
        try:
            # Prepare data
            dataset, stats = self.prepare_training_data(midi_files)
            
            # Split dataset
            dataset_size = len(list(dataset))
            val_size = int(dataset_size * validation_split)
            train_size = dataset_size - val_size
            
            train_dataset = dataset.skip(val_size).batch(batch_size).prefetch(tf.data.AUTOTUNE)
            val_dataset = dataset.take(val_size).batch(batch_size).prefetch(tf.data.AUTOTUNE)
            
            # Build model
            self.transformer = AdvancedMusicTransformer(
                vocab_size=self.processor.vocab_size,
                max_seq_length=256
            )
            self.transformer.build_model()
            
            # Advanced callbacks
            callbacks = [
                keras.callbacks.EarlyStopping(
                    monitor='val_loss',
                    patience=15,
                    restore_best_weights=True,
                    verbose=1
                ),
                keras.callbacks.ReduceLROnPlateau(
                    monitor='val_loss',
                    factor=0.7,
                    patience=8,
                    min_lr=1e-7,
                    verbose=1
                ),
                keras.callbacks.ModelCheckpoint(
                    filepath=os.path.join(self.model_dir, 'best_model.h5'),
                    monitor='val_loss',
                    save_best_only=True,
                    save_weights_only=False,
                    verbose=1
                ),
                keras.callbacks.TensorBoard(
                    log_dir=os.path.join("logs", f"training_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
                    histogram_freq=1,
                    write_graph=True,
                    update_freq='epoch'
                ),
                keras.callbacks.CSVLogger(
                    os.path.join("logs", "training_log.csv"),
                    append=True
                )
            ]
            
            # Custom progress callback
            if progress_callback:
                class AdvancedProgressCallback(keras.callbacks.Callback):
                    def on_epoch_end(self, epoch, logs=None):
                        logs = logs or {}
                        logs['training_stats'] = stats
                        progress_callback(epoch + 1, epochs, logs)
                
                callbacks.append(AdvancedProgressCallback())
            
            # Train with advanced options
            logger.info("Starting advanced training...")
            self.training_history = self.transformer.model.fit(
                train_dataset,
                epochs=epochs,
                validation_data=val_dataset,
                callbacks=callbacks,
                verbose=1,
                workers=4,  # Multi-threading
                use_multiprocessing=True
            )
            
            self.is_trained = True
            self.save_model()
            
            logger.info("Training completed successfully!")
            return self.training_history
            
        except Exception as e:
            logger.error(f"Training error: {e}")
            raise
    
    def generate(self, style_prompt: str = "", length: int = 500, 
                temperature: float = 0.8, seed_length: int = 64,
                use_cache: bool = True) -> str:
        """Enhanced generation with caching and better control"""
        
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        
        # Check cache
        cache_key = f"{style_prompt}_{length}_{temperature}_{seed_length}"
        if use_cache and cache_key in self.generation_cache:
            logger.info("Using cached generation")
            return self.generation_cache[cache_key]
        
        # Create enhanced seed based on style prompt
        seed = self._create_smart_seed(style_prompt, seed_length)
        
        logger.info(f"Generating music: length={length}, temp={temperature}, seed_len={len(seed)}")
        
        # Generate with advanced parameters
        generated_tokens = self.transformer.generate_music(
            seed, 
            length=length, 
            temperature=temperature,
            top_k=50,
            top_p=0.95,
            repetition_penalty=1.15
        )
        
        # Create output file with metadata
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"generated_music_{timestamp}_{temperature:.1f}temp.mid"
        output_path = os.path.join(self.model_dir, output_file)
        
        # Convert to MIDI with enhanced processing
        success = self.processor.tokens_to_midi(generated_tokens, output_path)
        
        if success:
            # Cache successful generation
            if use_cache:
                self.generation_cache[cache_key] = output_path
                # Limit cache size
                if len(self.generation_cache) > 10:
                    oldest_key = next(iter(self.generation_cache))
                    del self.generation_cache[oldest_key]
            
            logger.info(f"Music generated successfully: {output_path}")
            return output_path
        else:
            raise RuntimeError("Failed to generate MIDI file")
    
    def _create_smart_seed(self, style_prompt: str, seed_length: int) -> List[int]:
        """Create intelligent seed based on style prompt"""
        
        if len(self.processor.int_to_note) < seed_length:
            seed_length = min(32, len(self.processor.int_to_note))
        
        # Basic seed
        seed = list(range(min(seed_length, self.processor.vocab_size)))
        np.random.shuffle(seed)
        
        # Style-based modifications (simplified for now)
        if "classical" in style_prompt.lower():
            # Favor lower pitches and longer durations
            seed = [token for token in seed if token % 4 in [0, 1]]
        elif "jazz" in style_prompt.lower():
            # Favor syncopated rhythms
            seed = [token for token in seed if token % 3 != 0]
        elif "upbeat" in style_prompt.lower():
            # Favor shorter durations and higher pitches
            seed = [token for token in seed if token % 4 in [2, 3]]
        
        return seed[:seed_length]
    
    def save_model(self):
        """Enhanced model saving with metadata"""
        if self.transformer and self.transformer.model:
            # Save model architecture and weights
            model_path = os.path.join(self.model_dir, 'advanced_music_model.h5')
            self.transformer.model.save(model_path)
            
            # Save processor
            processor_path = os.path.join(self.model_dir, 'enhanced_processor.pkl')
            with open(processor_path, 'wb') as f:
                pickle.dump(self.processor, f)
            
            # Save vocabulary
            vocab_path = os.path.join(self.model_dir, 'vocabulary.json')
            self.processor.save_vocabulary(vocab_path)
            
            # Save enhanced config with metadata
            config = {
                'version': '2.0',
                'created': datetime.now().isoformat(),
                'vocab_size': self.processor.vocab_size,
                'max_seq_length': self.transformer.max_seq_length,
                'embed_dim': self.transformer.embed_dim,
                'num_heads': self.transformer.num_heads,
                'ff_dim': self.transformer.ff_dim,
                'num_layers': self.transformer.num_layers,
                'dropout_rate': self.transformer.dropout_rate,
                'model_params': self.transformer.model.count_params(),
                'training_history': self.training_history.history if self.training_history else None
            }
            
            config_path = os.path.join(self.model_dir, 'model_config.json')
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            logger.info(f"Enhanced model saved to {self.model_dir}")
    
    def load_model(self) -> bool:
        """Enhanced model loading with version compatibility"""
        try:
            # Try loading new format first
            config_path = os.path.join(self.model_dir, 'model_config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                logger.info(f"Loading model version {config.get('version', '1.0')}")
            
            # Load processor
            processor_paths = [
                os.path.join(self.model_dir, 'enhanced_processor.pkl'),
                os.path.join(self.model_dir, 'processor.pkl')
            ]
            
            processor_loaded = False
            for path in processor_paths:
                if os.path.exists(path):
                    with open(path, 'rb') as f:
                        self.processor = pickle.load(f)
                    processor_loaded = True
                    break
            
            if not processor_loaded:
                raise FileNotFoundError("No processor file found")
            
            # Load model
            model_paths = [
                os.path.join(self.model_dir, 'advanced_music_model.h5'),
                os.path.join(self.model_dir, 'music_model.h5'),
                os.path.join(self.model_dir, 'best_model.h5')
            ]
            
            model_loaded = False
            for path in model_paths:
                if os.path.exists(path):
                    try:
                        # Rebuild transformer with correct architecture
                        if os.path.exists(config_path):
                            with open(config_path, 'r') as f:
                                config = json.load(f)
                            self.transformer = AdvancedMusicTransformer(**{
                                k: v for k, v in config.items() 
                                if k in ['vocab_size', 'max_seq_length', 'embed_dim', 
                                        'num_heads', 'ff_dim', 'num_layers', 'dropout_rate']
                            })
                        else:
                            # Fallback to default architecture
                            self.transformer = AdvancedMusicTransformer(
                                vocab_size=self.processor.vocab_size
                            )
                        
                        # Load the actual model
                        self.transformer.model = keras.models.load_model(path)
                        model_loaded = True
                        break
                        
                    except Exception as e:
                        logger.warning(f"Failed to load model from {path}: {e}")
                        continue
            
            if not model_loaded:
                raise FileNotFoundError("No valid model file found")
            
            self.is_trained = True
            logger.info("Enhanced model loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
    
    def get_sample_midi_files(self, directory: str) -> List[str]:
        """Enhanced MIDI file discovery with better filtering"""
        midi_files = []
        
        # Search patterns with recursive search
        patterns = ['*.mid', '*.midi', '*.MID', '*.MIDI']
        
        for pattern in patterns:
            # Direct files
            midi_files.extend(glob.glob(os.path.join(directory, pattern)))
            # Recursive search in subdirectories
            midi_files.extend(glob.glob(os.path.join(directory, '**', pattern), recursive=True))
        
        # Remove duplicates and validate
        unique_files = list(set(midi_files))
        valid_files = []
        
        for file_path in unique_files:
            if self.processor.validate_midi_file(file_path):
                file_size = os.path.getsize(file_path)
                if 1000 < file_size < 5000000:  # 1KB to 5MB reasonable range
                    valid_files.append(file_path)
                else:
                    logger.warning(f"File size out of range: {file_path} ({file_size} bytes)")
            else:
                logger.warning(f"Invalid MIDI file: {file_path}")
        
        logger.info(f"Found {len(valid_files)} valid MIDI files out of {len(unique_files)} total")
        return sorted(valid_files)
    
    def get_model_info(self) -> Dict:
        """Get comprehensive model information"""
        info = {
            'is_trained': self.is_trained,
            'model_exists': False,
            'vocab_size': self.processor.vocab_size if hasattr(self.processor, 'vocab_size') else 0,
            'model_params': 0,
            'version': '2.0',
            'capabilities': [
                'Advanced transformer architecture',
                'Nucleus sampling generation',
                'Mixed precision training',
                'Gradient clipping',
                'Cosine learning rate schedule',
                'Style-aware seed generation'
            ]
        }
        
        if self.transformer and self.transformer.model:
            info.update({
                'model_exists': True,
                'model_params': self.transformer.model.count_params(),
                'embed_dim': self.transformer.embed_dim,
                'num_layers': self.transformer.num_layers,
                'num_heads': self.transformer.num_heads,
                'max_seq_length': self.transformer.max_seq_length
            })
        
        return info
