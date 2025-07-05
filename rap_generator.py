import random
import json

class ModernRapGenerator:
    def __init__(self):
        self.slang_2025 = [
            "no cap", "bussin", "fr fr", "periodt", "slay", "bet", "valid", 
            "it's giving", "understood the assignment", "main character energy",
            "living rent free", "that's fire", "absolutely sent me", "chef's kiss",
            "low-key", "high-key", "deadass", "straight up", "facts only",
            "that hits different", "absolutely unmatched", "pure excellence"
        ]
        
        self.modern_themes = [
            "crypto gains", "NFT flex", "streaming numbers", "going viral",
            "social media clout", "algorithm gaming", "digital nomad life",
            "sustainable fashion", "mindfulness journey", "self-care routine",
            "manifestation energy", "boundary setting", "toxic trait healing"
        ]
        
        self.rap_structures = {
            "verse": [
                "Started from the bottom now we {action}",
                "They don't understand the {concept}, no cap",
                "My {item} is {adjective}, that's just facts",
                "Living life {adverb}, {slang_phrase}",
                "Watch me {verb} like it's {year}",
                "This energy is {adjective}, periodt"
            ],
            "chorus": [
                "We stay {adjective}, that's the vibe",
                "{slang} all day, we don't hide",
                "Living {adverb}, feeling alive",
                "This is how we {verb} and thrive"
            ]
        }
        
        self.rhyme_pairs = [
            ("fire", "higher", "desire", "inspire"),
            ("vibe", "tribe", "pride", "ride"),
            ("flow", "grow", "show", "glow"),
            ("real", "feel", "deal", "steel"),
            ("way", "day", "say", "play")
        ]

    def generate_verse(self, bars=8):
        verse = []
        for _ in range(bars):
            template = random.choice(self.rap_structures["verse"])
            line = template.format(
                action=random.choice(["flexing", "winning", "grinding", "shining"]),
                concept=random.choice(self.modern_themes),
                item=random.choice(["energy", "mindset", "aesthetic", "journey"]),
                adjective=random.choice(["immaculate", "pristine", "iconic", "legendary"]),
                adverb=random.choice(["authentically", "unapologetically", "intentionally"]),
                slang_phrase=random.choice(self.slang_2025),
                verb=random.choice(["manifest", "elevate", "navigate", "innovate"]),
                year="2025"
            )
            verse.append(line)
        return verse

    def generate_full_song(self):
        song = {
            "intro": ["Yo, 2025 different, we evolved", "This that next level consciousness"],
            "verse1": self.generate_verse(8),
            "chorus": [
                "We stay bussin, that's the vibe",
                "No cap energy, we don't hide", 
                "Living authentically, feeling alive",
                "This is how we manifest and thrive"
            ],
            "verse2": self.generate_verse(8),
            "chorus_repeat": "// Repeat chorus",
            "bridge": [
                "From the metaverse to the real world",
                "We keep it 100, watch it unfurl",
                "Sustainable drip, conscious flex",
                "Generation Z, what's coming next?"
            ],
            "outro": ["That's how we close it out", "2025 style, no doubt"]
        }
        return song

    def format_song(self, song):
        formatted = ""
        for section, lines in song.items():
            if isinstance(lines, list):
                formatted += f"\n[{section.upper()}]\n"
                for line in lines:
                    formatted += f"{line}\n"
            else:
                formatted += f"\n[{section.upper()}]\n{lines}\n"
        return formatted

# Usage example
if __name__ == "__main__":
    generator = ModernRapGenerator()
    song = generator.generate_full_song()
    print(generator.format_song(song))
