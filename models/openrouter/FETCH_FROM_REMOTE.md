# OpenRouter Fetch-from-Remote 功能

## 概述

OpenRouter插件现在支持 `fetch-from-remote` 功能，允许用户在WebUI中填写API Key后自动获取所有可用的模型，无需手动添加每个模型配置。

## 功能特性

- ✅ **自动模型发现**: 填写API Key后自动获取所有可用模型
- ✅ **实时同步**: 自动同步OpenRouter最新模型列表
- ✅ **智能解析**: 自动识别模型功能（视觉、工具调用等）
- ✅ **定价信息**: 自动获取最新的模型定价信息
- ✅ **零维护**: 无需手动维护模型配置文件

## 使用方法

### 1. 在Dify中配置OpenRouter

1. 进入 **设置** → **模型供应商**
2. 找到 **OpenRouter** 供应商
3. 点击 **设置**
4. 填写您的 **API Key**（从 [OpenRouter](https://openrouter.ai/keys) 获取）
5. 点击 **保存**

### 2. 自动获取模型

配置完成后，系统会自动：
- 调用OpenRouter API获取所有可用模型
- 解析模型信息（名称、功能、定价等）
- 在模型选择界面显示所有可用模型

### 3. 使用模型

在应用配置中：
1. 选择 **OpenRouter** 作为模型供应商
2. 从自动获取的模型列表中选择所需模型
3. 开始使用

## 支持的模型功能

系统会自动识别以下模型功能：

- **Vision**: 支持图像理解的模型
- **Tool Call**: 支持工具调用的模型
- **Multi-Tool Call**: 支持多工具调用的模型

## 技术实现

### 配置方式

插件支持三种配置方式：
- `predefined-model`: 预定义模型
- `customizable-model`: 自定义模型
- `fetch-from-remote`: 从远程获取（新增）

### API调用

系统会调用以下OpenRouter API端点：
```
GET https://openrouter.ai/api/v1/models
```

### 数据转换

自动将OpenRouter API返回的模型信息转换为Dify格式：
- 模型ID和名称
- 上下文窗口大小
- 支持的功能特性
- 定价信息（转换为每百万token价格）

## 测试

可以使用提供的测试脚本验证功能：

```bash
# 设置API Key环境变量
export OPENROUTER_API_KEY=your_api_key_here

# 运行测试脚本
python test_fetch_models.py
```

## 故障排除

### 常见问题

1. **API Key无效**
   - 确保API Key正确且有效
   - 检查API Key是否有足够的权限

2. **网络连接问题**
   - 确保服务器可以访问 `https://openrouter.ai`
   - 检查防火墙设置

3. **模型列表为空**
   - 检查API Key是否有访问模型列表的权限
   - 查看日志获取详细错误信息

### 日志查看

在Dify日志中查找以下关键词：
- `OpenRouter`
- `fetch models`
- `get_models`

## 版本信息

- **插件版本**: 0.0.16
- **新增功能**: fetch-from-remote支持
- **依赖**: requests>=2.25.0

## 贡献

如果您发现问题或有改进建议，请：
1. 在GitHub上提交Issue
2. 提供详细的错误信息和日志
3. 描述预期行为和实际行为

---

**注意**: 此功能需要有效的OpenRouter API Key。请确保您的API Key有足够的权限访问模型列表。
