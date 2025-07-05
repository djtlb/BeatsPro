"""
Beat Addicts - Model Upgrade Examples
=====================================

This file demonstrates how to easily upgrade the AI lyrics generation model
to use better/more trained models. The system is designed for easy swapping
of AI models with minimal code changes.

UPGRADE METHODS:
1. Fine-tuned GPT-2 models (trained on lyrics)
2. Larger language models (GPT-3.5, GPT-4, Claude)  
3. Music-specialized models (MusicLM, AudioCraft)
4. Custom trained models
5. Multiple model ensemble
"""

import os
from typing import Dict, Any
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
try:
    import openai  # Example for OpenAI models
except ImportError:
    openai = None  # Will be None if not installed

# =============================================================================
# UPGRADE EXAMPLE 1: Fine-tuned GPT-2 Model (Trained on Lyrics)
# =============================================================================

class FineTunedLyricsGenerator:
    """
    Upgrade to a GPT-2 model fine-tuned specifically on song lyrics
    Simply replace the model path to use a better trained model
    """
    
    def __init__(self, model_path="./models/gpt2-lyrics-finetuned"):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Load fine-tuned model (just change the path!)
        if os.path.exists(model_path):
            print(f"Loading fine-tuned lyrics model from: {model_path}")
            self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
            self.model = GPT2LMHeadModel.from_pretrained(model_path)
        else:
            print("Fine-tuned model not found, using base GPT-2")
            self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
            self.model = GPT2LMHeadModel.from_pretrained('gpt2')
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Move model to device
        self.model.to(self.device)
        self.model.eval()

    def generate_lyrics(self, prompt="", theme="", mood="", **kwargs):
        """Same interface as original - no changes needed in app.py!"""
        # Enhanced prompt for fine-tuned model
        input_text = f"[THEME: {theme}] [MOOD: {mood}] [LYRICS] {prompt}"
        
        # Same generation logic as base model
        inputs = self.tokenizer.encode(input_text, return_tensors='pt').to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=len(inputs[0]) + kwargs.get('max_length', 200),
                temperature=kwargs.get('temperature', 0.8),
                top_p=kwargs.get('top_p', 0.9),
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                no_repeat_ngram_size=3,
                repetition_penalty=1.2  # Better for lyrics
            )
        
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        lyrics = generated_text[len(input_text):].strip()
        
        return {
            'lyrics': lyrics,
            'theme': theme,
            'mood': mood,
            'model_info': {'model_type': 'Fine-tuned GPT-2 (Lyrics)', 'enhanced': True}
        }


# =============================================================================
# UPGRADE EXAMPLE 2: OpenAI GPT-4 Integration
# =============================================================================

class OpenAILyricsGenerator:
    """
    Upgrade to use OpenAI's GPT-4 for superior lyrics generation
    Just set your API key and use this class instead!
    """
    
    def __init__(self, api_key=None):
        if openai is None:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        self.client = openai.OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        
    def generate_lyrics(self, prompt="", theme="", mood="", **kwargs):
        """Same interface - drop-in replacement!"""
        
        # Enhanced prompt engineering for GPT-4
        system_prompt = f"""You are a professional songwriter and lyricist. 
        Create original, creative lyrics that are:
        - Theme: {theme or 'General'}
        - Mood: {mood or 'Upbeat'}
        - Style: Modern, catchy, and emotionally resonant
        - Structure: Include verses, chorus, and bridge sections
        - Length: 2-3 verses with chorus
        """
        
        user_prompt = f"Write song lyrics starting with: {prompt}" if prompt else f"Write song lyrics about {theme}"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=kwargs.get('max_length', 400),
                temperature=kwargs.get('temperature', 0.8),
            )
            
            lyrics = response.choices[0].message.content
            
            return {
                'lyrics': lyrics,
                'theme': theme,
                'mood': mood,
                'model_info': {'model_type': 'GPT-4', 'provider': 'OpenAI', 'premium': True}
            }
            
        except Exception as e:
            return {
                'lyrics': f"Error with GPT-4: {str(e)}",
                'theme': theme,
                'mood': mood,
                'model_info': {'error': str(e)}
            }


# =============================================================================
# UPGRADE EXAMPLE 3: Multi-Model Ensemble
# =============================================================================

class EnsembleLyricsGenerator:
    """
    Use multiple models and combine their outputs for best results
    """
    
    def __init__(self):
        self.models = []
        
        # Initialize multiple models
        try:
            from ai_lyrics_generator import AILyricsGenerator
            self.models.append(('GPT-2', AILyricsGenerator()))
        except:
            pass
            
        # Add more models as available
        # self.models.append(('Fine-tuned', FineTunedLyricsGenerator()))
        # self.models.append(('GPT-4', OpenAILyricsGenerator()))
        
    def generate_lyrics(self, prompt="", theme="", mood="", **kwargs):
        """Generate from multiple models and pick the best"""
        
        results = []
        
        for model_name, model in self.models:
            try:
                result = model.generate_lyrics(prompt, theme, mood, **kwargs)
                result['model_name'] = model_name
                results.append(result)
            except Exception as e:
                print(f"Error with {model_name}: {e}")
        
        if not results:
            return {'lyrics': 'No models available', 'theme': theme, 'mood': mood}
        
        # For now, return the first successful result
        # In a real implementation, you could:
        # - Score lyrics quality
        # - Let user choose
        # - Combine parts from different models
        best_result = results[0]
        best_result['model_info']['ensemble'] = True
        best_result['model_info']['models_used'] = [r['model_name'] for r in results]
        
        return best_result


# =============================================================================
# UPGRADE EXAMPLE 4: Music-Specialized Model Integration
# =============================================================================

class MusicSpecializedGenerator:
    """
    Integration with music-specialized AI models like MusicLM or AudioCraft
    This would generate both lyrics AND music
    """
    
    def __init__(self):
        # This would initialize music generation models
        # For example: Meta's AudioCraft, Google's MusicLM, etc.
        self.lyrics_model = None  # Your lyrics model
        self.music_model = None   # Music generation model
        
    def generate_lyrics(self, prompt="", theme="", mood="", **kwargs):
        """Generate lyrics optimized for music generation"""
        
        # Enhanced lyrics with musical structure
        structured_prompt = f"""
        Create lyrics for a {mood} song about {theme}:
        - Include clear verse/chorus structure
        - Use rhythmic patterns suitable for music
        - Consider rhyme scheme and meter
        - Starting line: {prompt}
        """
        
        # This would use your preferred lyrics model
        # Plus add musical structure optimization
        
        return {
            'lyrics': "Generated lyrics with musical structure...",
            'theme': theme,
            'mood': mood,
            'musical_structure': {
                'verses': 3,
                'chorus': True,
                'bridge': True,
                'rhyme_scheme': 'ABAB'
            },
            'model_info': {'model_type': 'Music-Specialized', 'audio_ready': True}
        }


# =============================================================================
# HOW TO UPGRADE IN app.py (JUST CHANGE ONE LINE!)
# =============================================================================

def upgrade_instructions():
    """
    TO UPGRADE YOUR MODEL IN app.py:
    
    CURRENT CODE:
    from ai_lyrics_generator import AILyricsGenerator
    lyrics_generator = AILyricsGenerator()
    
    UPGRADE TO FINE-TUNED MODEL:
    from model_upgrade_examples import FineTunedLyricsGenerator
    lyrics_generator = FineTunedLyricsGenerator()
    
    UPGRADE TO GPT-4:
    from model_upgrade_examples import OpenAILyricsGenerator
    lyrics_generator = OpenAILyricsGenerator()
    
    UPGRADE TO ENSEMBLE:
    from model_upgrade_examples import EnsembleLyricsGenerator
    lyrics_generator = EnsembleLyricsGenerator()
    
    That's it! The interface stays the same, just better results!
    """
    pass


# =============================================================================
# EASY UPGRADE CONFIGURATION
# =============================================================================

def get_best_available_model():
    """
    Automatically select the best available model based on what's installed
    """
    
    # Priority order (best to worst)
    model_options = [
        ('OpenAI GPT-4', OpenAILyricsGenerator, lambda: os.getenv('OPENAI_API_KEY')),
        ('Fine-tuned GPT-2', FineTunedLyricsGenerator, lambda: os.path.exists('./models/gpt2-lyrics-finetuned')),
        ('Ensemble', EnsembleLyricsGenerator, lambda: True),
        ('Base GPT-2', None, lambda: True)  # Fallback
    ]
    
    for name, model_class, check_available in model_options:
        if check_available():
            print(f"Using model: {name}")
            return model_class() if model_class else None
    
    return None


# =============================================================================
# EXAMPLE: AUTOMATIC MODEL DETECTION
# =============================================================================

if __name__ == "__main__":
    # Test different model upgrades
    print("Testing model upgrades...")
    
    # Test base model
    try:
        from ai_lyrics_generator import AILyricsGenerator
        base_model = AILyricsGenerator()
        result = base_model.generate_lyrics("Love is in the air", "romance", "happy")
        print("Base GPT-2 Model:", result['model_info'])
    except Exception as e:
        print(f"Base model error: {e}")
    
    # Test automatic best model selection
    best_model = get_best_available_model()
    if best_model:
        result = best_model.generate_lyrics("Dancing in the moonlight", "party", "energetic")
        print("Best Available Model:", result.get('model_info', 'Unknown'))
    
    print("\nUpgrade system ready! See upgrade_instructions() for details.")
