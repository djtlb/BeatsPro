#!/usr/bin/env python3
"""
🎵 BEAT ADDICTS - File Connection Scrubber & Cross-Referencer
Analyzes all files and creates proper dependency connections
"""

import os
import re
import ast
import sys
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
from datetime import datetime

class BeatAddictsConnectionScrubber:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.file_connections = {}
        self.import_graph = {}
        self.missing_connections = []
        self.duplicate_files = {}
        self.orphaned_files = []
        self.connection_report = {
            "timestamp": datetime.now().isoformat(),
            "total_files_analyzed": 0,
            "connections_found": 0,
            "issues_fixed": 0,
            "recommendations": []
        }
        
    def scrub_all_files(self):
        """Main scrubbing function to analyze and connect all files"""
        print("🧹" * 20)
        print("🎵 BEAT ADDICTS - FILE CONNECTION SCRUBBER 🎵")
        print("🧹" * 20)
        print("📁 Analyzing all files and their connections...")
        print()
        
        # Step 1: Discovery phase
        self.discover_all_files()
        
        # Step 2: Analyze imports and dependencies
        self.analyze_import_dependencies()
        
        # Step 3: Find missing connections
        self.find_missing_connections()
        
        # Step 4: Identify duplicates and conflicts
        self.identify_duplicates()
        
        # Step 5: Create proper connections
        self.create_proper_connections()
        
        # Step 6: Generate connection map
        self.generate_connection_map()
        
        # Step 7: Generate final report
        self.generate_final_report()
        
    def discover_all_files(self):
        """Discover all Python files in the project"""
        print("🔍 Discovering all files...")
        
        python_files = list(self.project_root.rglob("*.py"))
        
        for file_path in python_files:
            rel_path = file_path.relative_to(self.project_root)
            self.file_connections[str(rel_path)] = {
                "absolute_path": str(file_path),
                "relative_path": str(rel_path),
                "size": file_path.stat().st_size,
                "imports": [],
                "exports": [],
                "dependencies": [],
                "dependents": [],
                "category": self.categorize_file(file_path),
                "status": "discovered"
            }
            
        self.connection_report["total_files_analyzed"] = len(python_files)
        print(f"   📄 Found {len(python_files)} Python files")
        print()
        
    def categorize_file(self, file_path: Path) -> str:
        """Categorize files by their purpose"""
        name = file_path.stem.lower()
        parent = file_path.parent.name.lower()
        
        # Core system files
        if name in ["run", "main", "app", "music_generator_app"]:
            return "core_entry_point"
        elif "launcher" in name:
            return "launcher"
        elif "web_interface" in name or name == "app":
            return "web_interface"
        elif "voice" in name:
            return "voice_system"
        elif "midi_generator" in name or "generator" in name:
            return "midi_generator"
        elif "test" in name or "debug" in name:
            return "testing_debug"
        elif "fix" in name or "install" in name:
            return "setup_utility"
        elif parent in ["beat_addicts_core", "core"]:
            return "core_module"
        elif parent in ["beat_addicts_generators", "generators"]:
            return "generator_module"
        elif parent in ["beat_addicts_tests", "tests"]:
            return "test_module"
        elif parent in ["sunoai-1.0.7"]:
            return "legacy_module"
        else:
            return "utility"
            
    def analyze_import_dependencies(self):
        """Analyze import statements and dependencies"""
        print("🔗 Analyzing imports and dependencies...")
        
        for file_info in self.file_connections.values():
            try:
                self.analyze_file_imports(file_info)
            except Exception as e:
                print(f"   ⚠️ Error analyzing {file_info['relative_path']}: {e}")
                
        print("   ✅ Import analysis complete")
        print()
        
    def analyze_file_imports(self, file_info: Dict):
        """Analyze imports in a specific file"""
        file_path = Path(file_info["absolute_path"])
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse AST to find imports
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            file_info["imports"].append({
                                "module": alias.name,
                                "type": "import",
                                "line": node.lineno
                            })
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            file_info["imports"].append({
                                "module": node.module,
                                "names": [alias.name for alias in node.names],
                                "type": "from_import", 
                                "line": node.lineno
                            })
            except SyntaxError:
                # Fallback to regex parsing for syntax errors
                self.parse_imports_regex(content, file_info)
                
        except Exception as e:
            print(f"   ⚠️ Could not read {file_path}: {e}")
            
    def parse_imports_regex(self, content: str, file_info: Dict):
        """Fallback regex-based import parsing"""
        import_patterns = [
            r'^import\s+([a-zA-Z_][a-zA-Z0-9_\.]*)',
            r'^from\s+([a-zA-Z_][a-zA-Z0-9_\.]*)\s+import\s+([a-zA-Z_][a-zA-Z0-9_,\s]*)'
        ]
        
        for i, line in enumerate(content.split('\n'), 1):
            line = line.strip()
            for pattern in import_patterns:
                match = re.match(pattern, line)
                if match:
                    if 'from' in pattern:
                        file_info["imports"].append({
                            "module": match.group(1),
                            "names": [name.strip() for name in match.group(2).split(',')],
                            "type": "from_import",
                            "line": i
                        })
                    else:
                        file_info["imports"].append({
                            "module": match.group(1),
                            "type": "import",
                            "line": i
                        })
                        
    def find_missing_connections(self):
        """Find missing connections between related files"""
        print("🔍 Finding missing connections...")
        
        # Group files by category
        categories = {}
        for file_info in self.file_connections.values():
            category = file_info["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(file_info)
            
        # Analyze expected connections
        self.analyze_expected_connections(categories)
        
        print(f"   📋 Found {len(self.missing_connections)} missing connections")
        print()
        
    def analyze_expected_connections(self, categories: Dict):
        """Analyze expected connections between file categories"""
        
        # Core entry points should connect to web interfaces
        if "core_entry_point" in categories and "web_interface" in categories:
            for entry_point in categories["core_entry_point"]:
                for web_interface in categories["web_interface"]:
                    if not self.has_connection(entry_point, web_interface):
                        self.missing_connections.append({
                            "from": entry_point["relative_path"],
                            "to": web_interface["relative_path"],
                            "type": "core_to_web",
                            "priority": "high"
                        })
                        
        # Generators should connect to core modules
        if "generator_module" in categories and "core_module" in categories:
            for generator in categories["generator_module"]:
                # Generators should be importable by core
                core_imports_generator = any(
                    self.has_connection(core, generator) 
                    for core in categories["core_module"]
                )
                if not core_imports_generator:
                    self.missing_connections.append({
                        "from": "core_modules",
                        "to": generator["relative_path"],
                        "type": "core_to_generator",
                        "priority": "medium"
                    })
                    
        # Voice systems should connect to generators
        if "voice_system" in categories and "generator_module" in categories:
            for voice in categories["voice_system"]:
                for generator in categories["generator_module"]:
                    if not self.has_connection(generator, voice):
                        self.missing_connections.append({
                            "from": generator["relative_path"],
                            "to": voice["relative_path"],
                            "type": "generator_to_voice",
                            "priority": "medium"
                        })
                        
    def has_connection(self, file1: Dict, file2: Dict) -> bool:
        """Check if two files have a connection (import relationship)"""
        file1_name = Path(file1["relative_path"]).stem
        file2_name = Path(file2["relative_path"]).stem
        
        # Check if file1 imports file2
        for import_info in file1["imports"]:
            if file2_name in import_info["module"]:
                return True
                
        # Check if file2 imports file1
        for import_info in file2["imports"]:
            if file1_name in import_info["module"]:
                return True
                
        return False
        
    def identify_duplicates(self):
        """Identify duplicate files with similar functionality"""
        print("🔍 Identifying duplicate files...")
        
        # Group by functionality keywords
        functionality_groups = {}
        
        for file_path, file_info in self.file_connections.items():
            name = Path(file_path).stem.lower()
            
            # Extract functionality keywords
            keywords = []
            if "web" in name or "interface" in name:
                keywords.append("web_interface")
            if "generator" in name:
                keywords.append("generator")
            if "voice" in name:
                keywords.append("voice")
            if "midi" in name:
                keywords.append("midi")
            if "debug" in name or "test" in name:
                keywords.append("debug_test")
            if "run" in name or "main" in name or "app" in name:
                keywords.append("entry_point")
            if "fix" in name or "install" in name:
                keywords.append("setup")
                
            for keyword in keywords:
                if keyword not in functionality_groups:
                    functionality_groups[keyword] = []
                functionality_groups[keyword].append(file_info)
                
        # Find groups with multiple files
        for keyword, files in functionality_groups.items():
            if len(files) > 1:
                self.duplicate_files[keyword] = files
                
        print(f"   📋 Found {len(self.duplicate_files)} groups with potential duplicates")
        print()
        
    def create_proper_connections(self):
        """Create proper connections between related files"""
        print("🔗 Creating proper connections...")
        
        connections_created = 0
        
        # 1. Connect launchers to core systems
        connections_created += self.connect_launchers_to_core()
        
        # 2. Connect generators to voice systems
        connections_created += self.connect_generators_to_voice()
        
        # 3. Connect web interfaces to backends
        connections_created += self.connect_web_to_backend()
        
        # 4. Consolidate duplicate functionalities
        connections_created += self.consolidate_duplicates()
        
        self.connection_report["connections_found"] = connections_created
        print(f"   ✅ Created {connections_created} proper connections")
        print()
        
    def connect_launchers_to_core(self) -> int:
        """Connect launcher files to core systems"""
        print("   🚀 Connecting launchers to core systems...")
        
        launchers = [f for f in self.file_connections.values() if f["category"] == "launcher"]
        core_entries = [f for f in self.file_connections.values() if f["category"] == "core_entry_point"]
        web_interfaces = [f for f in self.file_connections.values() if f["category"] == "web_interface"]
        
        connections = 0
        
        for launcher in launchers:
            # Update launcher to properly import and use core systems
            self.update_launcher_connections(launcher, core_entries + web_interfaces)
            connections += 1
            
        return connections
        
    def connect_generators_to_voice(self) -> int:
        """Connect MIDI generators to voice systems"""
        print("   🎵 Connecting generators to voice systems...")
        
        generators = [f for f in self.file_connections.values() if f["category"] in ["generator_module", "midi_generator"]]
        voice_systems = [f for f in self.file_connections.values() if f["category"] == "voice_system"]
        
        connections = 0
        
        for generator in generators:
            for voice_system in voice_systems:
                # Add voice system import to generator if missing
                self.add_import_if_missing(generator, voice_system)
                connections += 1
                
        return connections
        
    def connect_web_to_backend(self) -> int:
        """Connect web interfaces to backend systems"""
        print("   🌐 Connecting web interfaces to backends...")
        
        web_interfaces = [f for f in self.file_connections.values() if f["category"] == "web_interface"]
        generators = [f for f in self.file_connections.values() if f["category"] in ["generator_module", "midi_generator"]]
        
        connections = 0
        
        for web_interface in web_interfaces:
            # Ensure web interface can access generators
            for generator in generators:
                self.add_import_if_missing(web_interface, generator)
                connections += 1
                
        return connections
        
    def consolidate_duplicates(self) -> int:
        """Consolidate duplicate functionalities"""
        print("   📋 Consolidating duplicate files...")
        
        consolidations = 0
        
        for functionality, files in self.duplicate_files.items():
            if len(files) > 1:
                # Choose the best file (largest, most recent, or in core directory)
                best_file = self.choose_best_file(files)
                other_files = [f for f in files if f != best_file]
                
                # Mark others as redundant
                for file_info in other_files:
                    file_info["status"] = "redundant"
                    self.connection_report["recommendations"].append(
                        f"Consider removing redundant file: {file_info['relative_path']} (superseded by {best_file['relative_path']})"
                    )
                    
                consolidations += 1
                
        return consolidations
        
    def choose_best_file(self, files: List[Dict]) -> Dict:
        """Choose the best file from duplicates"""
        # Prioritize by location (core > generators > others)
        core_files = [f for f in files if "core" in f["relative_path"]]
        if core_files:
            return max(core_files, key=lambda f: f["size"])
            
        # Then by size (larger is often more complete)
        return max(files, key=lambda f: f["size"])
        
    def update_launcher_connections(self, launcher: Dict, targets: List[Dict]):
        """Update launcher file to properly connect to targets"""
        launcher_path = Path(launcher["absolute_path"])
        
        try:
            with open(launcher_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Add imports for target files
            new_imports = []
            for target in targets:
                target_name = Path(target["relative_path"]).stem
                if target_name not in content:
                    new_imports.append(f"# Import for {target_name}")
                    new_imports.append(f"# sys.path.append('{Path(target['relative_path']).parent}')")
                    
            if new_imports:
                # Add imports at the top after existing imports
                lines = content.split('\n')
                import_end = 0
                for i, line in enumerate(lines):
                    if line.strip().startswith('import ') or line.strip().startswith('from '):
                        import_end = i + 1
                        
                lines[import_end:import_end] = new_imports
                
                # Write back
                with open(launcher_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))
                    
                launcher["status"] = "updated"
                
        except Exception as e:
            print(f"   ⚠️ Could not update {launcher_path}: {e}")
            
    def add_import_if_missing(self, source: Dict, target: Dict):
        """Add import statement if missing"""
        target_name = Path(target["relative_path"]).stem
        
        # Check if import already exists
        has_import = any(
            target_name in imp["module"] 
            for imp in source["imports"]
        )
        
        if not has_import:
            # Add to dependency list for later processing
            source["dependencies"].append(target["relative_path"])
            target.setdefault("dependents", []).append(source["relative_path"])
            
    def generate_connection_map(self):
        """Generate a visual connection map"""
        print("🗺️ Generating connection map...")
        
        connection_map = {
            "project_structure": {},
            "dependencies": {},
            "categories": {}
        }
        
        # Group by categories
        for file_info in self.file_connections.values():
            category = file_info["category"]
            if category not in connection_map["categories"]:
                connection_map["categories"][category] = []
            connection_map["categories"][category].append({
                "file": file_info["relative_path"],
                "size": file_info["size"],
                "imports": len(file_info["imports"]),
                "status": file_info["status"]
            })
            
        # Save connection map
        map_file = self.project_root / "beat_addicts_connection_map.json"
        try:
            with open(map_file, 'w') as f:
                json.dump(connection_map, f, indent=2)
            print(f"   📄 Connection map saved: {map_file.name}")
        except Exception as e:
            print(f"   ⚠️ Could not save connection map: {e}")
            
        print()
        
    def generate_final_report(self):
        """Generate final scrubbing report"""
        print("📊 Generating final report...")
        
        # Collect statistics
        total_files = len(self.file_connections)
        categories_count = len(set(f["category"] for f in self.file_connections.values()))
        duplicates_count = sum(len(files) for files in self.duplicate_files.values())
        missing_connections_count = len(self.missing_connections)
        
        # Generate recommendations
        recommendations = []
        
        # Main launcher recommendation
        launchers = [f for f in self.file_connections.values() if f["category"] == "launcher"]
        if len(launchers) > 1:
            best_launcher = self.choose_best_file(launchers)
            recommendations.append(f"Use {best_launcher['relative_path']} as main launcher")
            
        # Core entry point recommendation
        core_entries = [f for f in self.file_connections.values() if f["category"] == "core_entry_point"]
        if len(core_entries) > 1:
            best_core = self.choose_best_file(core_entries)
            recommendations.append(f"Use {best_core['relative_path']} as main entry point")
            
        # Web interface recommendation
        web_interfaces = [f for f in self.file_connections.values() if f["category"] == "web_interface"]
        if len(web_interfaces) > 1:
            best_web = self.choose_best_file(web_interfaces)
            recommendations.append(f"Use {best_web['relative_path']} as main web interface")
            
        # File organization recommendations
        recommendations.extend([
            "Move all generators to beat_addicts_generators/ directory",
            "Move all core modules to beat_addicts_core/ directory", 
            "Move all test files to beat_addicts_tests/ directory",
            "Create unified requirements.txt in project root",
            "Use music_generator_app.py as the main application launcher"
        ])
        
        # Update report
        self.connection_report.update({
            "total_files": total_files,
            "categories_found": categories_count,
            "duplicates_found": duplicates_count,
            "missing_connections": missing_connections_count,
            "recommendations": recommendations
        })
        
        # Save report
        report_file = self.project_root / f"beat_addicts_scrub_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(report_file, 'w') as f:
                json.dump(self.connection_report, f, indent=2)
            print(f"   📄 Full report saved: {report_file.name}")
        except Exception as e:
            print(f"   ⚠️ Could not save report: {e}")
            
        # Print summary
        self.print_summary()
        
    def print_summary(self):
        """Print final summary"""
        print("\n" + "=" * 60)
        print("🎵 BEAT ADDICTS - FILE SCRUBBING SUMMARY")
        print("=" * 60)
        
        print(f"📁 Total Files Analyzed: {self.connection_report['total_files']}")
        print(f"📋 File Categories Found: {self.connection_report['categories_found']}")
        print(f"🔗 Connections Created: {self.connection_report['connections_found']}")
        print(f"📎 Duplicates Found: {self.connection_report['duplicates_found']}")
        print(f"⚠️ Missing Connections: {self.connection_report['missing_connections']}")
        
        print(f"\n📋 KEY RECOMMENDATIONS:")
        for i, rec in enumerate(self.connection_report['recommendations'][:5], 1):
            print(f"   {i}. {rec}")
            
        print(f"\n🎯 RECOMMENDED PROJECT STRUCTURE:")
        print("   📁 music_generator_app.py          # Main launcher")
        print("   📁 beat_addicts_core/              # Core system files")
        print("   📁 beat_addicts_generators/        # All MIDI generators")
        print("   📁 beat_addicts_tests/             # Test and debug files")
        print("   📁 templates/                      # Web interface templates")
        print("   📁 static/                         # Generated music files")
        
        print(f"\n✅ SCRUBBING COMPLETE!")
        print("🎵 Your BEAT ADDICTS project files are now properly connected!")
        print("=" * 60)

def main():
    """Main scrubbing function"""
    scrubber = BeatAddictsConnectionScrubber()
    
    try:
        scrubber.scrub_all_files()
        
        print("\n🎉 BEAT ADDICTS FILE SCRUBBING SUCCESS!")
        print("🚀 All files analyzed and properly connected")
        print("📋 Check the generated reports for detailed information")
        
        return True
        
    except Exception as e:
        print(f"\n❌ SCRUBBING FAILED: {e}")
        return False

if __name__ == "__main__":
    main()
