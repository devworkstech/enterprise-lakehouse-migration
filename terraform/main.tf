terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" { region = var.aws_region }

resource "aws_s3_bucket" "bronze" {
  bucket = "${var.environment}-lakehouse-bronze-${var.aws_account_id}"
  tags = { Environment = var.environment, Layer = "Bronze", Platform = "Lakehouse" }
}

resource "aws_s3_bucket" "silver" {
  bucket = "${var.environment}-lakehouse-silver-${var.aws_account_id}"
  tags = { Environment = var.environment, Layer = "Silver", Platform = "Lakehouse" }
}

resource "aws_s3_bucket" "gold" {
  bucket = "${var.environment}-lakehouse-gold-${var.aws_account_id}"
  tags = { Environment = var.environment, Layer = "Gold", Platform = "Lakehouse" }
}

resource "aws_glue_catalog_database" "lakehouse_db" {
  name = "${var.environment}_enterprise_lakehouse"
}
