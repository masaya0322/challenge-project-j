import subprocess
import os
import logging

class GameUpdater:
    def __init__(self, repo_path=None):
        self.repo_path = repo_path or os.path.dirname(os.path.abspath(__file__))
        self.logger = logging.getLogger(__name__)
    
    def check_for_updates(self):
        """更新があるかチェック"""
        try:
            subprocess.run(['git', 'fetch'], cwd=self.repo_path, check=True)
            
            local = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'], 
                cwd=self.repo_path
            ).decode().strip()
            
            remote = subprocess.check_output(
                ['git', 'rev-parse', 'origin/main'], 
                cwd=self.repo_path
            ).decode().strip()
            
            return local != remote
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Git操作エラー: {e}")
            return False
    
    def update(self):
        """更新実行"""
        try:
            result = subprocess.run(['git', 'pull'], cwd=self.repo_path, check=True)
            self.logger.info("ゲーム更新完了")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"更新エラー: {e}")
            return False