import os

def audit_repo(root_dir: str):
    print(f"Auditing repository at: {root_dir}")
    
    # 1. No large runtime artifacts (>50MB)
    # 2. No datasets (.csv except maybe submission.csv in root or output)
    # 3. No cache (__pycache__, .pytest_cache)
    # 4. No virtual environments (.venv, venv)
    # 5. No secrets (.env)
    # 6. No TODO/FIXME comments
    
    issues = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # ignore node_modules and .git to speed up
        if '.git' in dirnames:
            dirnames.remove('.git')
        if 'node_modules' in dirnames:
            dirnames.remove('node_modules')
        if '.next' in dirnames:
            dirnames.remove('.next')
        if 'venv' in dirnames:
            dirnames.remove('venv')
        if '.venv' in dirnames:
            dirnames.remove('.venv')
        if '__pycache__' in dirnames:
            dirnames.remove('__pycache__')
            
        rel_path = os.path.relpath(dirpath, root_dir)
        
        for d in dirnames:
            if d in ['__pycache__', '.pytest_cache', '.venv', 'venv', '.mypy_cache']:
                issues.append(f"Found cache/venv directory: {os.path.join(rel_path, d)}")
                
        for f in filenames:
            file_path = os.path.join(dirpath, f)
            rel_file_path = os.path.join(rel_path, f)
            
            # Check size
            try:
                size_mb = os.path.getsize(file_path) / (1024 * 1024)
                if size_mb > 50:
                    issues.append(f"Large file found (>50MB): {rel_file_path} ({size_mb:.2f}MB)")
            except:
                pass
                
            # Check for secrets / debug
            if f in ['.env', '.env.local', 'debug.log']:
                issues.append(f"Found secret/debug file: {rel_file_path}")
                
            # Check for datasets (naive check)
            if f.endswith('.csv') and 'submission' not in f.lower() and 'test' not in f.lower():
                issues.append(f"Possible dataset found: {rel_file_path}")
                
            # Check for TODO/FIXME in source code
            if f.endswith('.py') or f.endswith('.ts') or f.endswith('.tsx'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as src:
                        for line_num, line in enumerate(src):
                            if 'TODO' in line or 'FIXME' in line:
                                issues.append(f"TODO/FIXME found in {rel_file_path}:{line_num+1}")
                except Exception:
                    pass

    print("Audit Complete.")
    if issues:
        print(f"Found {len(issues)} issues:")
        for issue in issues:
            print(f" - {issue}")
    else:
        print("No issues found! Repository is clean.")

if __name__ == "__main__":
    audit_repo(".")
