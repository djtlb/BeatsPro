"""
AI Lyrics Generator for Beat Addicts
Streamlined GPT-2 based lyrics generation with easy model upgrade support
"""

import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import re
import os

class AILyricsGenerator:
    def __init__(self, model_path=None):
        """
        Initialize the lyrics generator
        
        Args:
            model_path (str, optional): Path to custom model. If None, uses default GPT-2
        """
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
        
        try:
            if model_path and os.path.exists(model_path):
                print(f"Loading custom model from: {model_path}")
                self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
                self.model = GPT2LMHeadModel.from_pretrained(model_path)
            else:
                print("Loading default GPT-2 model...")
                self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
                self.model = GPT2LMHeadModel.from_pretrained('gpt2')
            
            # Set pad token
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            self.model = self.model.to(self.device)
            self.model.eval()
            print("Model loaded successfully!")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def generate_lyrics(self, prompt="", theme="", mood="", max_length=200, temperature=0.8, top_p=0.9):
        """
        Generate lyrics based on prompt and parameters
        
        Args:
            prompt (str): Starting prompt for lyrics
            theme (str): Theme/topic for the song
            mood (str): Mood of the song
            max_length (int): Maximum length of generated text
            temperature (float): Creativity level (0.1-1.0)
            top_p (float): Nucleus sampling parameter
            
        Returns:
            dict: Generated lyrics with metadata
        """
        try:
            # Build the input prompt
            input_text = self._build_prompt(prompt, theme, mood)
            
            # Tokenize input
            inputs = self.tokenizer.encode(input_text, return_tensors='pt').to(self.device)
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=len(inputs[0]) + max_length,
                    temperature=temperature,
                    top_p=top_p,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    no_repeat_ngram_size=2,
                    repetition_penalty=1.1
                )
            
            # Decode and clean
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract just the generated part (remove input prompt)
            generated_lyrics = generated_text[len(input_text):].strip()
            
            # Clean and format lyrics
            lyrics = self._clean_lyrics(generated_lyrics)
            
            return {
                'lyrics': lyrics,
                'theme': theme or 'General',
                'mood': mood or 'Neutral',
                'prompt_used': input_text,
                'model_info': {
                    'model_type': 'GPT-2',
                    'temperature': temperature,
                    'top_p': top_p
                }
            }
            
        except Exception as e:
            print(f"Error generating lyrics: {e}")
            return {
                'lyrics': f"Sorry, I couldn't generate lyrics right now. Error: {str(e)}",
                'theme': theme or 'General',
                'mood': mood or 'Neutral',
                'prompt_used': input_text if 'input_text' in locals() else prompt,
                'model_info': {'error': str(e)}
            }

    def _build_prompt(self, prompt, theme, mood):
        """Build a structured prompt for better lyrics generation"""
        base_prompt = ""
        
        if theme:
            base_prompt += f"Song about {theme}. "
        if mood:
            base_prompt += f"Mood: {mood}. "
        
        # Add lyrics structure hints
        base_prompt += "Lyrics:\n"
        
        if prompt:
            base_prompt += f"{prompt}\n"
        
        return base_prompt

    def _clean_lyrics(self, text):
        """Clean and format the generated lyrics"""
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        
        # Remove incomplete sentences at the end
        sentences = text.split('.')
        if len(sentences) > 1 and len(sentences[-1].strip()) < 10:
            text = '.'.join(sentences[:-1]) + '.'
        
        # Limit length and ensure it ends properly
        lines = text.split('\n')
        if len(lines) > 20:  # Limit to reasonable length
            lines = lines[:20]
            text = '\n'.join(lines)
        
        # Ensure it doesn't end mid-word
        if text and not text[-1] in '.!?':
            last_complete = max(text.rfind('.'), text.rfind('!'), text.rfind('?'))
            if last_complete > len(text) * 0.7:  # If we find a sentence end in the last 30%
                text = text[:last_complete + 1]
        
        return text.strip()

    def get_model_info(self):
        """Get information about the current model"""
        return {
            'model_type': 'GPT-2',
            'device': str(self.device),
            'tokenizer_vocab_size': len(self.tokenizer),
            'model_parameters': sum(p.numel() for p in self.model.parameters()),
            'upgradeable': True,
            'supported_upgrades': [
                'Fine-tuned GPT-2 models',
                'Larger GPT models (GPT-3.5, GPT-4)',
                'Music-specialized models',
                'Custom trained models'
            ]
        }
