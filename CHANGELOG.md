# CHANGELOG

## [1.6.0] - 2026-04-02

### Added
- 新增配置系统支持（`_conf_schema.json`）
  - `max_image_size`: 可配置最大图片大小（字节），默认 5MB
  - `allowed_paths`: 可配置允许访问的路径白名单列表
  - `enable_path_restriction`: 可配置是否启用路径限制功能

### Enhanced
- 路径限制检查功能
  - 使用 `pathlib.Path.relative_to()` 方法进行安全的路径检查
  - 避免 `startswith()` 方法的目录穿越漏洞
  - 使用 `Path.resolve()` 解析符号链接和绝对路径

### Fixed
- 修复 `is_relative_to()` 返回值未判断的逻辑 Bug
- 配置参数类型注解修正为 `dict | None`

### Notes
- 配置项可通过 AstrBot 管理界面进行设置
- 留空 `allowed_paths` 列表时，路径限制功能允许访问所有路径（仅限制大小）