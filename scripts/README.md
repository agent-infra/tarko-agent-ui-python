# Release Scripts

## auto_release.py

优化的 Python 包发布流程脚本，实现完整的自动化发布工作流。

### 功能特性

1. **智能版本管理**
   - 自动决策下个要发布的版本（patch 版本 +1）
   - 创建 `release/{version}` 分支
   - Python 包和 npm 版本保持一致

2. **静态资源管理**
   - 拉取 npm 最新包或指定版本
   - 清理旧产物确保干净构建
   - 自动构建和验证静态资源

3. **完整发布流程**
   - 自动创建 git tag
   - 推送到远程仓库
   - 发布到 PyPI
   - 自动回到原始分支

4. **安全保障**
   - 运行测试套件确保质量
   - 干净的构建环境
   - 错误处理和回滚机制

### 使用方法

```bash
# 查看帮助
python3 scripts/auto_release.py --help

# 预览发布计划（推荐）
python3 scripts/auto_release.py --dry-run

# 使用最新 npm 版本发布
python3 scripts/auto_release.py

# 指定 npm 版本发布
python3 scripts/auto_release.py --npm-version 0.3.0-beta.15

# 跳过测试（不推荐）
python3 scripts/auto_release.py --skip-tests

# 只构建不发布（用于测试）
python3 scripts/auto_release.py --skip-publish
```

### 发布流程详解

1. **准备阶段**
   - 获取当前分支信息
   - 确定 npm 和 Python 版本
   - 显示发布计划

2. **分支管理**
   - 切换到 main 分支并拉取最新代码
   - 创建 `release/{version}` 分支

3. **构建阶段**
   - 清理旧的构建产物
   - 更新版本文件
   - 下载并构建静态资源
   - 运行测试套件
   - 构建 Python 包

4. **发布阶段**
   - 提交更改并创建 tag
   - 推送到远程仓库
   - 发布到 PyPI

5. **清理阶段**
   - 切换回原始分支

### 版本同步策略

- **Python 版本**: 自动 bump patch 版本（如 0.3.2 → 0.3.3）
- **npm 版本**: 使用指定版本或最新版本
- **版本记录**: 在 `__init__.py` 中同时记录两个版本

### 错误处理

- 任何步骤失败都会停止流程
- 自动切换回原始分支
- 详细的错误信息和日志
- 支持中断恢复

### 依赖要求

- Python 3.8+
- uv (Python 包管理器)
- git
- 网络连接（访问 npm registry 和 PyPI）

### 最佳实践

1. **发布前检查**
   ```bash
   # 先运行 dry-run 检查计划
   python3 scripts/auto_release.py --dry-run
   ```

2. **测试构建**
   ```bash
   # 只构建不发布，验证构建过程
   python3 scripts/auto_release.py --skip-publish
   ```

3. **版本控制**
   - 确保在 main 分支上进行发布
   - 发布前确保所有更改已提交
   - 使用语义化版本号

4. **质量保证**
   - 不要跳过测试（除非紧急情况）
   - 验证静态资源正确构建
   - 检查发布后的包是否可用
