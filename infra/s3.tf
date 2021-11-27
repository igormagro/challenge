resource "aws_s3_bucket" "buckets" {
  count  = length(var.bucket_names)
  bucket = "${local.prefix}-${var.bucket_names[count.index]}"
  acl    = "private"

  tags = var.tags

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

resource "aws_s3_bucket" "scripts" {
  bucket = "370799417405-scripts"

  acl = "private"

  tags = var.tags

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}
