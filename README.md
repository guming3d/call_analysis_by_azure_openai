# Call Analysis Project

## Overview

This project is designed to transcribe audio files, analyze the transcriptions using Azure OpenAI, and generate reports in both Excel and Markdown formats. The primary use case is to review the effectiveness of sales calls and provide feedback for improvement.

## Architecture Diagram

![Architecture Diagram](architecture/calling_analyze.drawio.png)

## Setup

1. **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd EF_call_analysis
    ```

2. **Create a virtual environment:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory with the following content:

    ```plaintext
    AZURE_SUBSCRIPTION_KEY=<your_azure_subscription_key>
    AZURE_REGION=<your_azure_region>
    AZURE_OPENAI_ENDPOINT=<your_azure_openai_endpoint>
    AZURE_OPENAI_DEPLOYMENT_NAME=<your_azure_openai_deployment_name>
    AZURE_OPENAI_API_KEY=<your_azure_openai_api_key>
    ```

## Usage

1. **Place audio files:**

    Place your audio files (in `.mp3` or `.wav` format) in the `./audios` directory.

2. **Run the project:**

    ```bash
    ./run.sh
    ```

3. **Check the output:**

    The transcriptions and analysis results will be saved in the `./output` directory. Reports will be generated as `report.xlsx` and `report.md`.

## View the Report

To view the report in a web interface, you can use the `report_display.py` script which utilizes Streamlit to render the JSON content in a table format.

screenshot:
![screenshot](screenshot/screenshot.jpeg)

1. **Run the Streamlit app:**

    ```bash
    streamlit run report_display.py
    ```

2. **Open the provided URL in your browser to view the report.**

## View the Report

To view the report in a web interface, you can use the `report_display.py` script which utilizes Streamlit to render the JSON content in a table format.

1. **Run the Streamlit app:**

    ```bash
    streamlit run report_display.py
    ```

2. **Open the provided URL in your browser to view the report.**

## 中文说明

### 概述

该项目旨在转录音频文件，使用 Azure OpenAI 分析转录内容，并生成 Excel 和 Markdown 格式的报告。主要用例是审查销售电话的有效性，并提供改进反馈。

### 先决条件

- Python 3.12 或更高版本
- pip (Python 包安装器)
- 具有 Azure 认知服务和 Azure OpenAI 访问权限的 Azure 订阅

### 设置

1. **克隆仓库:**

    ```bash
    git clone <repository_url>
    cd EF_call_analysis
    ```

2. **创建虚拟环境:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **安装依赖项:**

    ```bash
    pip install -r requirements.txt
    ```

4. **设置环境变量:**

    在根目录中创建一个 `.env` 文件，内容如下：

    ```plaintext
    AZURE_SUBSCRIPTION_KEY=<your_azure_subscription_key>
    AZURE_REGION=<your_azure_region>
    AZURE_OPENAI_ENDPOINT=<your_azure_openai_endpoint>
    AZURE_OPENAI_DEPLOYMENT_NAME=<your_azure_openai_deployment_name>
    AZURE_OPENAI_API_KEY=<your_azure_openai_api_key>
    ```

### 查看报告

要在 Web 界面中查看报告，您可以使用 `report_display.py` 脚本，该脚本利用 Streamlit 以表格格式呈现 JSON 内容。

截图:
![screenshot](screenshot/screenshot.jpeg)

1. **运行 Streamlit 应用程序:**

    ```bash
    streamlit run report_display.py
    ```

2. **在浏览器中打开提供的 URL 以查看报告。**

### 使用方法

1. **放置音频文件:**

    将您的音频文件（格式为 `.mp3` 或 `.wav`）放置在 `./audios` 目录中。

2. **运行项目:**

    ```bash
    ./run.sh
    ```

3. **检查输出:**

    转录和分析结果将保存在 `./output` 目录中。报告将生成为 `report.xlsx` 和 `report.md` 文件。
