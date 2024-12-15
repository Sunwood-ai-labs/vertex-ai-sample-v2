from google.cloud import aiplatform
import os
from dotenv import load_dotenv

def verify_connection():
    """Vertex AIとの接続を確認するための関数"""
    try:
        # 環境変数の読み込み
        load_dotenv()
        project = os.getenv('GOOGLE_CLOUD_PROJECT')
        location = os.getenv('GOOGLE_CLOUD_REGION')

        # プロジェクトの初期化
        aiplatform.init(
            project=project,
            location=location
        )
        
        # 利用可能なモデルのリストを取得（疎通確認として）
        models = aiplatform.Model.list()
        print("✅ 接続成功！")
        print(f"📁 プロジェクト: {project}")
        print(f"🌏 リージョン: {location}")
        return True
        
    except Exception as e:
        print("❌ エラーが発生しました:")
        print(e)
        return False

if __name__ == "__main__":
    verify_connection()
