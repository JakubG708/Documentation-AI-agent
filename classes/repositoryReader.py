import os
import subprocess

class RepositoryReader:
    def __init__(self, repository, language_extensions):
        self.repository = repository
        self.assignation = {}
        self.language_extensions = language_extensions

    def is_ignored_by_git(self, file_path):
        try:
            # subprocess zwraca 0 jeśli plik jest ignorowany
            result = subprocess.run(
                ['git', 'check-ignore', file_path],
                cwd=self.repository,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Nie udało się sprawdzić .gitignore dla {file_path}: {e}")
            return False

    def readRepoFiles(self):
        for root, dirs, files in os.walk(self.repository):
            for file in files:
                ext = os.path.splitext(file)[1]
                file_path = os.path.join(root, file)

                if ext in self.language_extensions and not self.is_ignored_by_git(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        self.assignation[file_path] = content
                    except Exception as e:
                        print(f"Nie można odczytać pliku {file_path}: {e}")

                        
reader = RepositoryReader("C:\\Users\\agnel\\Desktop\\ai_agent_project\\Documentation-AI-agent", [".py"])

reader.readRepoFiles()

print(reader.assignation.keys())
print("\n\n\n\n\n")
print(reader.assignation.items())
