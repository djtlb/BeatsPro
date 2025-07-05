import random
import json

class ModernRapGenerator:
    def __init__(self):
        self.slang_2025 = [
            "no cap", "bussin", "fr fr", "periodt", "slay", "bet", "valid", 
            "it's giving", "understood the assignment", "main character energy",
            "living rent free", "that's fire", "absolutely sent me", "chef's kiss",
            "low-key", "high-key", "deadass", "straight up", "facts only",
            "that hits different", "absolutely unmatched", "pure excellence",
            "ate and left no crumbs", "mother is mothering", "serving looks",
            "touch grass", "ratio", "based", "cringe", "mid", "W take", "L behavior"
        ]
        
        self.modern_themes = [
            "crypto gains", "NFT flex", "streaming numbers", "going viral",
            "social media clout", "algorithm gaming", "digital nomad life",
            "sustainable fashion", "mindfulness journey", "self-care routine",
            "manifestation energy", "boundary setting", "toxic trait healing",
            "main character arc", "side quest completed", "level up energy"
        ]
        
        self.rap_flows = {
            "aggressive": [
                "I'm {adjective} with the {noun}, {slang}",
                "They can't handle my {theme}, straight facts",
                "Pulling up with that {adjective} energy, no discussion",
                "This is how we {verb} in {year}, periodt"
            ],
            "melodic": [
                "Floating through life so {adjective}",
                "My {theme} got me feeling {emotion}",
                "We just {verb} different, you know",
                "Living this {adjective} lifestyle, {slang}"
            ],
            "trap": [
                "Got that {adjective} flow, yeah",
                "{noun} in my hand, we don't play",
                "All my people stay {adjective}, facts",
                "Money, power, {theme}, that's the way"
            ]
        }

    def generate_bars(self, style="aggressive", count=16):
        bars = []
        flow_templates = self.rap_flows[style]
        
        for i in range(count):
            template = random.choice(flow_templates)
            bar = template.format(
                adjective=random.choice(["immaculate", "iconic", "legendary", "pristine", "unmatched"]),
                noun=random.choice(["vision", "energy", "mindset", "aesthetic", "vibe"]),
                slang=random.choice(self.slang_2025),
                theme=random.choice(self.modern_themes),
                verb=random.choice(["manifest", "elevate", "navigate", "dominate", "innovate"]),
                year="2025",
                emotion=random.choice(["blessed", "motivated", "unstoppable", "grateful"])
            )
            bars.append(f"{i+1:2d}. {bar}")
        
        return bars

    def create_full_song(self, title="Untitled"):
        return {
            "title": title,
            "intro": [
                "Yeah, 2025 different breed",
                "This that evolution you need",
                "Let me show you how we proceed"
            ],
            "verse1": self.generate_bars("aggressive", 16),
            "hook": [
                "We stay bussin, that's the vibe (that's the vibe)",
                "No cap energy, we don't hide (we don't hide)",
                "Living authentically, certified (certified)",
                "This is how we manifest and ride (and ride)"
            ],
            "verse2": self.generate_bars("melodic", 16),
            "bridge": [
                "From the metaverse to reality",
                "We keep it 100, that's the key",
                "Generation Alpha energy",
                "This the future, can't you see?"
            ],
            "outro": [
                "That's how we close it, no debate",
                "2025 style, sealed our fate",
                "Pure excellence, don't you wait"
            ]
        }

    def export_lyrics(self, song):
        output = f"🎤 {song['title'].upper()} 🎤\n\n"
        
        for section, lines in song.items():
            if section == "title":
                continue
            
            output += f"[{section.upper()}]\n"
            if isinstance(lines, list):
                for line in lines:
                    output += f"{line}\n"
            output += "\n"
        
        return output

# Example usage
if __name__ == "__main__":
    generator = ModernRapGenerator()
    song = generator.create_full_song("Digital Flex")
    print(generator.export_lyrics(song))
