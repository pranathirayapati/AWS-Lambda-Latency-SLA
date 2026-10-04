# AWS Lambda with Provisioned Concurrency for Latency SLA

## Project Overview

This project studies latency in AWS Lambda-based serverless applications and evaluates the use of Provisioned Concurrency to reduce the impact of cold starts.

## Problem Statement

AWS Lambda may experience additional latency when a new execution environment needs to be created and initialized. These cold starts can increase response time and affect latency-sensitive applications.

## Objective

The main objective is to study Lambda latency and evaluate whether Provisioned Concurrency can improve tail latency.

## SLA

Our target SLA is:

P95 latency <= 300 ms

P95 represents the latency value below which approximately 95% of requests are completed.

## Architecture

Python Load Tester
        |
        v
API Gateway
        |
        v
AWS Lambda
        |
        v
Application Response
        |
        v
CloudWatch

## AWS Services Used

- AWS Lambda
- Amazon API Gateway
- AWS IAM
- Amazon CloudWatch

## Testing

The Python load-testing script sends 100 requests and measures:

- Average latency
- P95 latency
- P99 latency
- SLA compliance

## API Endpoints

POST /baseline

POST /optimized

## Technologies

- Python
- AWS Lambda
- API Gateway
- CloudWatch
- GitHub

## Project Status

The project includes the Lambda implementation, API Gateway integration and Python-based latency testing framework.

Provisioned Concurrency evaluation depends on the available AWS account concurrency quota.