# プロジェクトIDの設定
$PROJECT_ID = "terraform-sandbox-444503"

Write-Host "🔧 必要なAPIを有効化しています..." -ForegroundColor Green
gcloud services enable aiplatform.googleapis.com --project $PROJECT_ID
gcloud services enable compute.googleapis.com --project $PROJECT_ID
gcloud services enable iam.googleapis.com --project $PROJECT_ID
gcloud services enable artifactregistry.googleapis.com --project $PROJECT_ID

# サービスアカウントの設定
$SA_NAME = "vertex-ai-user"
$SA_EMAIL = "$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com"

Write-Host "👤 サービスアカウントを作成しています..." -ForegroundColor Green
gcloud iam service-accounts create $SA_NAME `
    --description="Vertex AI operations service account" `
    --display-name="Vertex AI User" `
    --project $PROJECT_ID

Write-Host "🔑 必要なロールを付与しています..." -ForegroundColor Green
gcloud projects add-iam-policy-binding $PROJECT_ID `
    --member="serviceAccount:$SA_EMAIL" `
    --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID `
    --member="serviceAccount:$SA_EMAIL" `
    --role="roles/storage.objectViewer"

Write-Host "🗝️ サービスアカウントのキーを生成しています..." -ForegroundColor Green
gcloud iam service-accounts keys create vertex-ai-key.json `
    --iam-account=$SA_EMAIL `
    --project $PROJECT_ID

Write-Host "✅ セットアップが完了しました！" -ForegroundColor Green
Write-Host "📝 以下の環境変数を.envファイルに設定してください：" -ForegroundColor Yellow
Write-Host "GOOGLE_APPLICATION_CREDENTIALS=$(Get-Location)\vertex-ai-key.json"
Write-Host "GOOGLE_CLOUD_PROJECT=$PROJECT_ID"
Write-Host "GOOGLE_CLOUD_REGION=asia-northeast1"
