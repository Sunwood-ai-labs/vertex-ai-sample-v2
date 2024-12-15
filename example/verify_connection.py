from google.cloud import aiplatform
from google.cloud import aiplatform_v1
import os
from dotenv import load_dotenv
from loguru import logger
from art import tprint

def verify_connection():
    """Vertex AIとの接続を確認し、利用可能なモデルとエンドポイントを表示する関数"""
    try:
        # アスキーアートでタイトルを表示
        tprint("Vertex AI", font="block")
        logger.info("Vertex AI 接続確認を開始します")

        # 環境変数の読み込み
        load_dotenv()
        project = os.getenv('GOOGLE_CLOUD_PROJECT')
        location = os.getenv('GOOGLE_CLOUD_REGION')

        if not project or not location:
            logger.error("❌ 環境変数が設定されていません")
            logger.error("GOOGLE_CLOUD_PROJECT と GOOGLE_CLOUD_REGION を設定してください")
            return False

        # プロジェクトの初期化
        aiplatform.init(
            project=project,
            location=location
        )
        
        # 接続情報のログ出力
        logger.success("✅ 接続成功！")
        logger.info(f"📁 プロジェクト: {project}")
        logger.info(f"🌏 リージョン: {location}")
        
        # ModelServiceClientを使用してモデル一覧を取得
        try:
            client = aiplatform_v1.ModelServiceClient()
            parent = client.common_location_path(project, location)
            request = aiplatform_v1.ListModelsRequest(
                parent=parent
            )
            logger.info("🤖 利用可能なモデル一覧:")
            page_result = client.list_models(request=request)
            model_count = 0
            for model in page_result:
                model_count += 1
                logger.info(f"- 名前: {model.display_name}")
                logger.info(f"  ID: {model.name}")
                logger.info(f"  説明: {model.description if model.description else 'なし'}")
                logger.info("  ---")
            
            if model_count == 0:
                logger.warning("⚠️ モデルが見つかりませんでした")
                logger.info("Vertex AI コンソールでモデルをデプロイしてください")
        
        except Exception as e:
            logger.error("❌ モデル一覧の取得中にエラーが発生しました:")
            logger.error(str(e))

        # エンドポイント一覧を取得
        try:
            endpoint_client = aiplatform_v1.EndpointServiceClient()
            parent = endpoint_client.common_location_path(project, location)
            endpoint_request = aiplatform_v1.ListEndpointsRequest(
                parent=parent
            )
            logger.info("🎯 利用可能なエンドポイント一覧:")
            endpoint_result = endpoint_client.list_endpoints(request=endpoint_request)
            endpoint_count = 0
            for endpoint in endpoint_result:
                endpoint_count += 1
                logger.info(f"- 名前: {endpoint.display_name}")
                logger.info(f"  ID: {endpoint.name}")
                logger.info("  ---")
            
            if endpoint_count == 0:
                logger.warning("⚠️ エンドポイントが見つかりませんでした")
        
        except Exception as e:
            logger.error("❌ エンドポイント一覧の取得中にエラーが発生しました:")
            logger.error(str(e))

        # 使用可能なモデルリソースの一覧を取得
        try:
            logger.info("📋 使用可能なモデルリソース一覧:")
            for model_type in aiplatform.Model.list_model_resources():
                logger.info(f"- {model_type}")
        except Exception as e:
            logger.error("❌ モデルリソース一覧の取得中にエラーが発生しました:")
            logger.error(str(e))

        return True
        
    except Exception as e:
        logger.error("❌ 予期せぬエラーが発生しました:")
        logger.error(str(e))
        return False

if __name__ == "__main__":
    # 接続確認の実行
    verify_connection()
