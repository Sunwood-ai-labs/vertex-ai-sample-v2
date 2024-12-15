# プロジェクトID
$PROJECT_ID = "terraform-sandbox-444503"

Write-Host "🔍 IAM権限の確認中..." -ForegroundColor Green
gcloud projects get-iam-policy $PROJECT_ID --format=yaml

Write-Host "`n📋 有効化されているAPIの確認中..." -ForegroundColor Green
gcloud services list --project $PROJECT_ID --enabled

Write-Host "`n🤖 Vertex AIモデルの確認中..." -ForegroundColor Green
gcloud ai models list --region=asia-northeast1

Write-Host "`n🎯 Vertex AIエンドポイントの確認中..." -ForegroundColor Green
gcloud ai endpoints list --region=asia-northeast1
