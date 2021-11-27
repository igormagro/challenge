resource "aws_s3_bucket_object" "dist" {
  for_each = fileset("../kubernetes/spark/scripts/", "*.py")

  bucket = aws_s3_bucket.scripts.bucket
  key    = "spark-scripts/${each.value}"
  source = "../kubernetes/spark/scripts/${each.value}"

  etag = filemd5("../kubernetes/spark/scripts/${each.value}")

  tags = var.tags
}