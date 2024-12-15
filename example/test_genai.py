from google import generativeai as genai
import os
from dotenv import load_dotenv
from loguru import logger
from art import tprint
from pathlib import Path

def test_genai(prompt="今日のご飯を提案して"):
    """Google GenAI クライアントを使用してテキストを生成する関数"""
    try:
        # アスキーアートでタイトルを表示
        tprint("Google GenAI", font="block")
        
        # プロジェクトルートの.envを読み込む
        project_root = Path(__file__).parent.parent
        dotenv_path = project_root / '.env'
        load_dotenv(dotenv_path)
        
        project = os.getenv('GOOGLE_CLOUD_PROJECT')
        location = os.getenv('GOOGLE_CLOUD_REGION')

        if not project or not location:
            logger.error("❌ 環境変数が設定されていません")
            logger.error(f"📁 .envファイルの場所: {dotenv_path}")
            logger.error("GOOGLE_CLOUD_PROJECT と GOOGLE_CLOUD_REGION を設定してください")
            return None

        # クライアントの初期化
        logger.info("🚀 Google GenAI クライアントの初期化中...")
        logger.info(f"📁 プロジェクト: {project}")
        logger.info(f"🌏 リージョン: {location}")
        
        try:
            genai.configure(
                project=project,  # project_id から project に変更
                location=location,
                credentials=None  # 既存の認証情報を使用
            )
        except Exception as auth_error:
            logger.error("❌ 認証エラーが発生しました")
            logger.error("以下のコマンドを実行して認証を行ってください:")
            logger.error("gcloud auth application-default login --scopes=\"https://www.googleapis.com/auth/cloud-platform\"")
            raise auth_error

        # モデルの設定
        logger.info("🤖 モデルの設定中...")
        model = genai.GenerativeModel('gemini-pro')

        # テキスト生成
        logger.info(f"📝 プロンプト: {prompt}")
        logger.info("📤 生成されたテキスト:")
        
        response = model.generate_content(prompt, stream=True)
        
        for chunk in response:
            print(chunk.text, end="")

        logger.success("\n✅ テキスト生成が完了しました")

    except Exception as e:
        logger.error("❌ エラーが発生しました:")
        logger.error(str(e))
        return None

if __name__ == "__main__":
    # テストの実行
    test_genai()
