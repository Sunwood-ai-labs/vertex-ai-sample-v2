from google.cloud import aiplatform
import vertexai
from vertexai.language_models import TextGenerationModel
import vertexai.generative_models as generative_models
import os
from dotenv import load_dotenv
from loguru import logger
from art import tprint
from pathlib import Path

def test_gemini(prompt="What's a good name for a flower shop that specializes in selling bouquets of dried flowers?"):
    """Gemini APIを使用してテキストを生成する関数"""
    try:
        # アスキーアートでタイトルを表示
        tprint("Vertex AI", font="block")
        
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

        # Vertex AI の初期化
        logger.info("🚀 Vertex AIの初期化中...")
        logger.info(f"📁 プロジェクト: {project}")
        logger.info(f"🌏 リージョン: {location}")
        vertexai.init(project=project, location=location)

        # Geminiモデルの初期化
        logger.info("🤖 Geminiモデルの読み込み中...")
        model = generative_models.GenerativeModel("gemini-1.0-pro")

        # テキスト生成
        logger.info(f"📝 プロンプト: {prompt}")
        response = model.generate_content(prompt)

        # 結果の出力
        logger.success("✅ テキスト生成が完了しました")
        logger.info("📤 生成されたテキスト:")
        print(response.text)

        return response.text

    except Exception as e:
        logger.error("❌ エラーが発生しました:")
        logger.error(str(e))
        return None

if __name__ == "__main__":
    # テストの実行
    test_gemini()
