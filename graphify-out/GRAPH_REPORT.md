# Graph Report - .  (2026-07-16)

## Corpus Check
- 148 files · ~124,926 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1791 nodes · 2967 edges · 178 communities (95 shown, 83 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 162 edges (avg confidence: 0.65)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Video Pipeline Core
- Video Pipeline Tests
- TTS Providers
- TTS Tests
- BGM Service
- Subtitle Service
- Material Service
- Video Effects
- LLM Provider Models
- LLM Provider Tests
- LLM Live Integration Tests
- Material Tests
- Sonilo Service
- Task Manager Base/Memory
- BGM Tests
- Upload Post Service
- Utils Module
- Voice Providers
- Controller Video Tests
- Video Controller v1
- CLI Interface
- Agent Skill Tests
- Base Controller & Exceptions
- Video Service Core
- WebUI BGM Tests
- WebUI Main App
- Version Checker & WebUI Task Ops
- Subtitle Tests
- Schema Models & Material Service
- Video Transition Tests
- TTS Providers (Chatterbox/ElevenLabs/Gemini/MiMo)
- Config & LLM Provider Models
- Voice Provider Detection
- Video Combine/FFmpeg
- LLM Provider Tests
- Video Tests
- Config Module
- Video Service Tests
- Project Docs & AI Agent
- ASGI App & Ping
- BGM Service Tests
- LLM Script Prompt Tests
- Redis Task Manager Tests
- Controller Base Tests
- External Dependencies
- Controller Video Helper Tests
- Subtitle Background Tests
- ElevenLabs Voice Tests
- Voice Service Tests
- WebUI i18n Tests
- Task Manager Base
- TwelveLabs Service
- Video Effects Utils
- LLM Social Metadata Tests
- TwelveLabs Tests
- WebUI Task History Tests
- LLM Gateway & Dependencies
- Config Persistence Tests
- LLM Connection Tests
- WebUI Fonts & Task Restore
- Sponsor SVG (PicWish)
- Video Schema & LLM Controller Tests
- Azure TTS v2 & Subtitle Formatter
- Subtitle Item Builders
- Docker Compose & Dockerfile
- Sponsor SVG (RecCloud)
- Ollama Provider Tests
- Qwen Provider Tests
- LLM Provider Spec
- GitHub CI/CD & Redis
- WebUI Segmented Controls
- Video Social Metadata
- LLM Tutorial Transcripts
- SynchronizedConfig Dict Ops
- WebUI Script Settings
- Runtime Environment Detection
- LiteLLM Provider Edge Cases
- TwelveLabs Live Tests
- Video Material Resolution Tests
- WebUI Task Restore
- GitHub Issue Templates
- Docker Release & Publish
- Transcript Placeholders
- LLM Video Concepts
- Video Combine Speed Tests
- Video Aspect Schema
- Video SubclippedClip
- Create Project Tutorials
- Tutorial Website References
- Test Structure & Coverage
- AGENTS.md Graphify
- Subtitle Font Support
- OpenCode Plugin Graphify
- WebUI Entry
- YouTube Outro Next Video
- YouTube Outro Subscribe
- BytePlus Sponsor
- GitHub Security Policy
- OpenCode Plugin Graphify
- App Init
- Voice Silent Audio
- Voice Audio Duration
- AI Laptops Data
- Data Value Identification
- Microsoft Word Chinese
- Docker GPU Compose
- Cubence Sponsor
- VolcEngine Sponsor
- MiMo Provider Test
- Default Model Names
- Provider Registry Unique IDs
- Provider Registry Order
- Provider Registry Locale Keys
- Registry Deprecated Models
- Provider Tip Templates
- Primary Provider Tips
- Required API Key Providers
- Config Duplicates
- Removed Ernie Provider
- Pollinations API Key
- Pollinations Unified API
- Cloudflare Account ID
- Cloudflare AI Gateway
- OpenAI Credentials Redaction
- AIHubMix Provider
- Evolink Provider
- BGM Project Relative Path
- BGM Path Security
- FFmpeg Binary Env Path
- FFmpeg Fallback
- Video Codec Default
- Video Codec Preserve
- FFmpeg Encoder Fallback
- VideoFile Fallback
- FFmpeg Concat Path Normalize
- Concat Fallback
- Concat Codec Fallback
- Combine Videos Audio Duration
- Transition Mode None
- Combine Videos Duration Margin
- Concat Audio Duration Limit
- Unique Source Clips
- Wrap Text Test
- Rounded Subtitle Background
- Voice Audio Duration Non-MP3
- Voice Audio Duration Missing
- Voice No Voice Alias
- Voice Non-ASCII Duration
- Voice Silent Audio Reject
- Voice Empty Name
- Azure TTS v1 Legacy Edge
- Azure TTS v1 Timeout
- Azure TTS v2 SSML
- Azure TTS v2 Rate Forward
- Gemini TTS GenAI
- MiMo TTS OpenAI Compatible
- Chatterbox Voice Helpers
- Chatterbox TTS Endpoint
- Chatterbox TTS Base URL
- Chatterbox HTTP Error
- Voice No Voice Silent
- Edge Cue Thousand Separator
- Arabic Script Split
- Arabic Letter Forms
- Arabic Variant Forms
- Subtitle Ignore Markdown Sep
- Subtitle Ignore Underscore
- Compshare Logo
- WebUI Screenshot
- Pkg MoneyPrinterTurbo
- Test Resource Images

## God Nodes (most connected - your core abstractions)
1. `VideoParams` - 63 edges
2. `TestLiteLLMProvider` - 51 edges
3. `TestTaskService` - 47 edges
4. `TestVideoService` - 39 edges
5. `HttpException` - 37 edges
6. `TestCli` - 37 edges
7. `TestVoiceService` - 35 edges
8. `MemoryState` - 33 edges
9. `MaterialInfo` - 26 edges
10. `_render_audio_settings()` - 23 edges

## Surprising Connections (you probably didn't know these)
- `Transcript Placeholder Content (tutorial.com, LLM references)` --sample_output_of--> `Video Generation Pipeline`  [AMBIGUOUS]
  graphify-out/transcripts/output005.txt → README.md
- `TestVideoControllerFiles` --uses--> `TaskQueueFullError`  [INFERRED]
  test/services/test_controller_video.py → app/controllers/manager/base_manager.py
- `TestVideoControllerHelpers` --uses--> `TaskQueueFullError`  [INFERRED]
  test/services/test_controller_video.py → app/controllers/manager/base_manager.py
- `TestVideoControllerTasks` --uses--> `TaskQueueFullError`  [INFERRED]
  test/services/test_controller_video.py → app/controllers/manager/base_manager.py
- `TestRedisTaskManager` --uses--> `TaskQueueFullError`  [INFERRED]
  test/services/test_task_manager.py → app/controllers/manager/base_manager.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **MoneyPrinterTurbo Core Architecture** — moneyprinterturbo_ai_video_generator, webui_streamlit_webui, api_fastapi_api, cli_py_cli_interface, ai_agent_workflow, video_generation_pipeline [EXTRACTED 0.95]
- **CI/CD Pipeline** — github_workflows_ci_ci_workflow, github_workflows_docker_ghcr_docker_publish_workflow, github_workflows_ci_python_versions, github_workflows_ci_redis_service, github_workflows_ci_uv_package_manager, github_workflows_ci_ruff_linter, github_workflows_ci_pytest_coverage, github_workflows_ci_windows_smoke_tests, docker_publish_ghcr_multiplatform, docker_publish_buildkit_cache [EXTRACTED 0.95]
- **Docker Deployment Stack** — dockerfile_docker_build, docker_compose_yml_local_dev_compose, docker_compose_gpu_yml_gpu_override, docker_compose_release_yml_release_compose, docker_compose_webui_api_services, docker_compose_shared_volumes, docker_compose_gpu_nvidia_runtime, docker_compose_release_prebuilt_image, docker_compose_release_config_storage_volumes, dockerfile_python_311_slim_bullseye, dockerfile_ffmpeg_git, dockerfile_mirror_support, dockerfile_pip_mirror_support, dockerfile_streamlit_cmd [EXTRACTED 0.95]
- **Video Generation Python Dependencies** — requirements_txt_dependencies, moviepy_video_editing, streamlit_webui_framework, edge_tts_tts_provider, fastapi_api_framework, uvicorn_asgi_server, openai_sdk, faster_whisper_asr, loguru_logging, google_genai_gemini_sdk, dashscope_qwen_sdk, azure_cognitiveservices_speech_tts, redis_client, pydub_audio_processing, litellm_llm_gateway [EXTRACTED 1.00]
- **AI Agent Skill Ecosystem** — docs_skill_skill_md_ai_agent_skill, mpt_agent_py_agent_helper, docs_skill_skill_md_skill_definition, uv_python_manager, config_toml_configuration, pexels_api_footage, exit_codes_agent_workflow [EXTRACTED 0.95]
- **GitHub Governance Templates** — github_issue_template_bug_report_bug_report, github_issue_template_feature_request_feature_request, github_issue_template_config_blank_issues_disabled, github_security_security_policy, github_issue_template_bug_report_template_bilingual, github_issue_template_feature_request_template_bilingual, blank_issues_disabled, github_security_policy_supported_versions, github_security_policy_private_reporting [EXTRACTED 0.95]
- **Test Infrastructure** — test_readme_md_test_documentation, test_structure_services, test_pytest_unittest_compat, test_coverage_pytest_cov, test_integration_mpt_run_integration_tests, github_workflows_ci_pytest_coverage, github_workflows_ci_windows_smoke_tests [EXTRACTED 0.95]
- **TTS and Subtitle Generation Ecosystem** — tts_providers, edge_tts_tts_provider, azure_cognitiveservices_speech_tts, subtitle_generation_edge_whisper, faster_whisper_asr, edge_tts_voice_list, docs_voice_list_txt_edge_tts_voices [INFERRED 0.90]
- **LLM Provider and Gateway Ecosystem** — llm_providers, llm_gateways, openai_sdk, google_genai_gemini_sdk, dashscope_qwen_sdk, litellm_llm_gateway [INFERRED 0.85]
- **Transcript Test Artifacts (graphify-out)** — graphify_out_transcripts_output005_txt_transcript, graphify_out_transcripts_output008_txt_transcript, graphify_out_transcripts_output015_txt_transcript, graphify_out_transcripts_output017_txt_transcript, graphify_out_transcripts_output021_txt_transcript, transcript_placeholder_content [INFERRED 0.70]
- **Logo Layer Stack** — docs_sponsors_reccloud_logo_outer_circle, docs_sponsors_reccloud_logo_middle_ring, docs_sponsors_reccloud_logo_inner_circle, docs_sponsors_reccloud_logo_accent_shape [INFERRED 0.90]
- **RecCloud Brand Identity Elements** — docs_sponsors_reccloud_logo_reccloud_brand, docs_sponsors_reccloud_logo_outer_circle, docs_sponsors_reccloud_logo_middle_ring, docs_sponsors_reccloud_logo_inner_circle, docs_sponsors_reccloud_logo_accent_shape [INFERRED 0.95]
- **LLM Tutorial Video Cluster** — graphifyout_transcripts_output004_llm_tutorial, graphifyout_transcripts_output013_llm_tutorial, graphifyout_transcripts_output028_llm_tutorial, graphifyout_transcripts_output022_llm_tutorial, graphifyout_transcripts_output010_llm_tutorial, graphifyout_transcripts_output002_llm_tutorial, graphifyout_transcripts_output020_llm_tutorial [INFERRED 0.95]
- **Create New Project Tutorial Cluster** — graphifyout_transcripts_output000_create_project, graphifyout_transcripts_output024_create_project, graphifyout_transcripts_output016_create_project, graphifyout_transcripts_output018_create_project [INFERRED 0.95]
- **YouTube Outro Pattern Cluster** — graphifyout_transcripts_output001_youtube_outro, graphifyout_transcripts_output007_youtube_outro, graphifyout_transcripts_output003_youtube_outro, graphifyout_transcripts_output023_youtube_outro [INFERRED 0.95]
- **Tutorial Website Reference Cluster** — graphifyout_transcripts_output009_www_tutorial_com, graphifyout_transcripts_output019_www_tutorial_com, graphifyout_transcripts_output027_www_tutorial_com, graphifyout_transcripts_output006_www_tutorial_com [INFERRED 0.95]
- **LLM Video Tutorial Transcripts** — graphify_out_transcripts_output029_video_about_llms, graphify_out_transcripts_output014_video_about_llms, graphify_out_transcripts_output029_llm_concept, graphify_out_transcripts_output014_llm_concept, graphify_out_transcripts_output029_video_tutorial_concept, graphify_out_transcripts_output014_video_tutorial_concept [INFERRED 0.85]

## Communities (178 total, 83 thin omitted)

### Community 0 - "Video Pipeline Core"
Cohesion: 0.04
Nodes (30): {       "video_subject": "",       "video_aspect": "横屏 16:9（西瓜视频）",       "voice, VideoParams, 判断字幕文字和背景是否同色，提醒用户可能无法看清字幕。, subtitle_colors_are_indistinguishable(), TestClipSpeed, 首次状态写入失败时不能静默退出，也不能继续消耗发布额度。, 状态后端短暂失败一次后应继续发布，并最终保存完成状态。, Sonilo 必须针对每条拼接后的视频生成配乐，并传给最终混音。 (+22 more)

### Community 1 - "Video Pipeline Tests"
Cohesion: 0.07
Nodes (49): correct(), create(), file_to_subtitles(), levenshtein_distance(), similarity(), _ensure_cross_post_terminal_state(), _finalize_cross_post_future(), generate_audio() (+41 more)

### Community 2 - "TTS Providers"
Cohesion: 0.08
Nodes (51): apply_environment_config(), ensure_config(), ensure_project(), generate_video(), has_cli_option(), _has_configured_value(), log(), main() (+43 more)

### Community 3 - "TTS Tests"
Cohesion: 0.05
Nodes (8): After preprocess_video, material.url should be an absolute path, not a bare file, 启用自定义 BGM 时仍必须在任务启动前报告缺少文件。, 0 音量应忽略缺失或无效文件，与 WebUI 和视频服务保持一致。, CLI 必须跟随 BGM 服务的格式白名单，不能继续单独限制为 MP3。, 非法格式或越界路径应转换为包含统一格式范围的 CLI 错误。, 帮助命令应独立于业务配置加载，便于用户查看和脚本采集。, 任务服务返回结构化失败信息时，CLI 仍必须以非零状态退出。, TestCli

### Community 4 - "BGM Service"
Cohesion: 0.07
Nodes (15): _event(), 公开文档的连字符写法必须归一化为项目内部服务标识。, 200 响应缺少规范服务列表时不能向 WebUI 报告连接成功。, 提供 requests.Response 在 Sonilo 服务中实际使用的最小接口。, 连接测试的网络中断和非 JSON 响应都转换为稳定的领域异常。, 成功代理必须去音轨、限制尺寸，并由调用方接管生成文件。, FFmpeg 超时、不可执行或编码失败时均不能遗留隐藏代理文件。, FFmpeg 返回成功也必须再次校验代理文件存在、非空且未超上限。 (+7 more)

### Community 5 - "Subtitle Service"
Cohesion: 0.07
Nodes (12): ABC, BaseState, Convert values written by this application back to common Python types., 只更新已有任务的指定字段；任务不存在时返回 False。, Redis-backed task state.      Trust boundary: Redis is expected to be private to, RedisState, _FakeRedis, Redis SCAN 分批返回 key 时，分页切片必须按当前批次起始位置计算。          这个用例复现 PR #890 描述的 18 条任务、page (+4 more)

### Community 6 - "Material Service"
Cohesion: 0.07
Nodes (17): AsyncUpdateChecker, get_available_update(), _parse_version(), 检查 MoneyPrinterTurbo 是否存在可用的新正式版本。, 后台版本检查的即时状态，供 WebUI 无阻塞地读取。, 在后台线程中执行版本检查，并缓存最近一次结果。      Streamlit 会在任意控件交互后从头执行页面脚本。如果直接在标题区域访问     GitHub，, 立即返回检查快照；缓存过期时在后台启动一次新检查。, 兼容 GitHub 常用的 ``v1.2.3`` 标签并转换为可比较版本。 (+9 more)

### Community 7 - "Video Effects"
Cohesion: 0.09
Nodes (26): clean_video_cache(), get_video_cache_stats(), _is_cleanup_candidate(), _iter_video_cache_entries(), 即使缓存目录为空，也应稳定拒绝无效清理参数。, 统计全部缓存，或预览修改时间早于指定天数的可清理缓存。      ``max_age_days=None`` 表示全部缓存。统计过程只读取目录项的大小和修改时间, 清理默认视频缓存，并返回可向用户展示的汇总结果。      页面预览与真正点击清理之间可能间隔较久，所以执行时必须重新扫描和判断，     不能复用旧候选列表。, 缓存目录的轻量统计结果，只包含文件系统元数据。 (+18 more)

### Community 8 - "LLM Provider Models"
Cohesion: 0.07
Nodes (13): MemoryState, 异步发布更新不能覆盖已经完成的视频任务字段。, TestMemoryState, 发布工作异常退出时也必须归还容量，避免后续发布永久被拒绝。, 启动恢复只处理遗留状态，当前进程仍持有的发布任务不能被误伤。, worker 已结束但状态仍活动时，最终回调必须补写失败终态。, 排队 Future 被取消时也必须释放容量并写入失败终态。, 发布队列满载时必须保留成片，并且不能继续向线程池提交任务。 (+5 more)

### Community 9 - "LLM Provider Tests"
Cohesion: 0.12
Nodes (28): generate_video_script(), generate_video_social_metadata(), generate_video_terms(), Request, BaseResponse, BgmRetrieveResponse, BgmUploadResponse, _Config (+20 more)

### Community 10 - "LLM Live Integration Tests"
Cohesion: 0.14
Nodes (30): build_script_prompt(), build_social_metadata_prompt(), _clamp_text(), _extract_chat_completion_text(), _extract_qwen_generation_text(), _fallback_social_metadata(), _generate_response(), generate_script() (+22 more)

### Community 11 - "Material Tests"
Cohesion: 0.06
Nodes (14): download_videos 可能被服务层或测试直接传入字符串模式，而不是         VideoConcatMode 枚举。这里用空搜索词避免真实网络请, 开启按文案顺序匹配素材后，不能让第一个关键词的多个候选先把         音频时长填满。这里模拟两个关键词各有多个候选，验证下载顺序是         ter, Coverr 视频素材源(spec: 2026-06-09-coverr-video-provider-design.md)。     全部用 unittest, search_videos_coverr 应把每个 hit 转成 MaterialInfo，并把 urls.mp4_download         直接作为, 与 pexels/pixabay 一致:未显式配置时 TLS 校验默认开启。, 企业自签证书代理场景必须能显式关闭 TLS 校验。, Coverr duration 字段在不同响应里可能是 number 或 string,         两种格式都要接受;低于 minimum_duratio, 默认路径必须开启 TLS 校验，避免素材 API key 和返回的素材 URL         在公共网络或不可信代理环境中被中间人攻击截获或篡改。 (+6 more)

### Community 12 - "Sonilo Service"
Cohesion: 0.12
Nodes (29): _base_url(), _create_video_proxy(), generate_bgm(), get_api_key(), is_enabled(), _normalize_service_id(), _parse_event(), Any (+21 more)

### Community 13 - "Task Manager Base/Memory"
Cohesion: 0.11
Nodes (12): ValueError, TaskQueueFullError, InMemoryTaskManager, 任务执行入口必须启动线程，并把函数参数完整传给 run_task。, 内存队列应保持函数、位置参数和关键字参数，不得改变任务内容。, 并发名额用尽后允许排队到上限，超过上限才返回明确错误。, 并发名额必须在线程启动前预占；即使 mock 的线程尚未进入 run_task，         第二个请求也应进入队列，不能突破 max_concurrent, 线程启动失败不能永久占用并发名额，异常仍应交给调用方处理。 (+4 more)

### Community 14 - "BGM Tests"
Cohesion: 0.12
Nodes (28): BgmServiceError, BgmUploadError, list_bgm_files(), RuntimeError, ValueError, 仅使用项目当前配置的 FFmpeg 验证文件包含可完整解码的音频流。      项目允许 imageio-ffmpeg 提供便携 FFmpeg，该安装方式不保证, 校验磁盘上的音频文件可由项目 FFmpeg 完整解码。      上传预检通常只需 30 秒；Sonilo 生成的配乐最长可达 6 分钟，因此对外提供, 将上传流写入同目录临时文件，并返回安全文件名、临时路径和字节数。      WebUI 的上传预检和最终持久化必须使用完全相同的分块读取、大小限制与文件名 (+20 more)

### Community 15 - "Upload Post Service"
Cohesion: 0.13
Nodes (14): cross_post_video(), Upload-Post API integration for cross-posting videos to TikTok, Instagram and Yo, Check the status of an upload request.          Args:             request_id (st, UploadPostService, _get(), _get_all(), _has_key(), _mock_response() (+6 more)

### Community 16 - "Utils Module"
Cohesion: 0.08
Nodes (20): get_ffmpeg_binary(), get_response(), normalize_clip_speed(), normalize_script_for_subtitle_matching(), public_dir(), Any, 解析当前进程应该使用的 FFmpeg 可执行文件。      增加原因：     1. 视频编码、静音音频生成、pydub 音频转码都依赖 FFmpeg；, 清理字幕匹配前的脚本文本。      用户可能手动输入 Markdown 分隔符、标题强调或 `_` 这类格式符号。     这些字符通常不会出现在 TTS/W (+12 more)

### Community 17 - "Voice Providers"
Cohesion: 0.10
Nodes (25): azure_tts_v1(), convert_rate_to_percent(), create_edge_tts_communicate(), estimate_no_voice_duration(), get_all_azure_voices(), get_chatterbox_voices(), get_edge_tts_timeout_seconds(), get_elevenlabs_voices() (+17 more)

### Community 18 - "Controller Video Tests"
Cohesion: 0.10
Nodes (12): 创建任务应持久化初始状态，并把原请求模型与停止阶段交给队列。, 队列已满时必须回滚刚创建的状态，并向调用方返回 429。, 任务列表响应必须包含状态层返回的总数和请求分页参数。, endpoint 未配置时应返回相对任务 URL，且不能把展示用 URL 回写到状态，         否则后续请求可能基于已改写数据重复拼接路径。, 失败阶段和错误信息必须通过任务查询接口原样返回。, OpenAPI 模型示例必须覆盖发布成功和生成失败两种状态。, 生成中和发布中的任务都在读取目录，删除接口必须返回 409。, 查询或删除未知任务都应返回一致的 404，而不是空成功响应。 (+4 more)

### Community 19 - "Video Controller v1"
Cohesion: 0.18
Nodes (24): create_audio(), create_subtitle(), create_task(), create_video(), delete_video(), download_video(), get_all_tasks(), get_bgm_list() (+16 more)

### Community 20 - "CLI Interface"
Cohesion: 0.14
Nodes (23): _bgm_type(), build_video_params(), _CliHelpFormatter, _hex_color(), _non_negative_float(), _paragraph_count(), parse_args(), _path_is_within_directory() (+15 more)

### Community 21 - "Agent Skill Tests"
Cohesion: 0.12
Nodes (6): FakeHttpResponse, Path, 生成失败时保留模型原始错误，避免 Skill 层猜测供应商语义。, 创建足够完成安装和配置检查的最小项目结构。, 确保 Windows Agent 不会在命令中嵌入易被破坏的绝对路径。, TestMptAgentSkill

### Community 22 - "Base Controller & Exceptions"
Cohesion: 0.14
Nodes (15): get_api_key(), get_task_id(), Request, verify_token(), _sanitize_upload_filename(), upload_bgm_file(), upload_video_material_file(), FileNotFoundException (+7 more)

### Community 23 - "Video Service Core"
Cohesion: 0.13
Nodes (22): close_clip(), _escape_ffmpeg_concat_path(), _format_ffmpeg_concat_path(), generate_video(), get_bgm_file(), _get_temp_audio_dir(), _get_visible_center_position(), _hex_to_rgb() (+14 more)

### Community 24 - "WebUI BGM Tests"
Cohesion: 0.22
Nodes (8): 0 音量保留上传选择，但必须等重新启用 BGM 后才校验和预览。, 选择 Sonilo 后应回填本机 Key，但控件必须保持密码显示模式。, Sonilo 音量为 0 时，WebUI 不应继续显示 API Key 必填警告。, 生成一个很短的标准 WAV，避免测试依赖仓库外部音频或系统录音文件。, 按测试语言读取期望文案，避免断言反过来依赖某一种展示语言。, 通过稳定业务 key 查找控件，展示标签翻译后仍能命中同一控件。, TestWebuiBackgroundMusic, _valid_wav_bytes()

### Community 25 - "WebUI Main App"
Cohesion: 0.14
Nodes (19): _active_generation_tasks(), _add_active_generation_task(), _build_uploaded_file_path(), _delete_task(), _detect_audio_mime(), _dismiss_settings_dialog(), get_tts_provider_tips(), _get_unmet_restore_upload_requirements() (+11 more)

### Community 26 - "Version Checker & WebUI Task Ops"
Cohesion: 0.15
Nodes (21): poll_available_update(), 读取全局后台检查器状态，避免不同 Streamlit 会话重复请求 GitHub。, _collect_task_summaries(), _count_processing_tasks(), _format_task_time(), _normalize_task_state(), _open_task_path(), _open_task_video() (+13 more)

### Community 27 - "Subtitle Tests"
Cohesion: 0.10
Nodes (10): Whisper 可能把一句文案拆成多个时间块。校正逻辑应合并时间范围并恢复         原始脚本文本，避免最终字幕出现不必要的碎片。, 转写结果与脚本完全不一致时仍应以脚本为准；脚本多出的句子没有可复用         时间轴时使用明确的零时间占位，避免丢失文本且保持现有兼容行为。, The final subtitle must be parsed even when the SRT file does not end         wi, A normal SRT ending in a blank line still parses all blocks., 字幕校正依赖编辑距离选择是否继续合并相邻字幕，因此覆盖空字符串、         参数交换、大小写忽略和明显不相似四种边界，防止算法调整后误合并。, 可选 Whisper 依赖未安装时应跳过，而不是在任务线程中抛异常。, 模型下载或初始化失败时必须返回失败结果，并允许任务层更新状态。, 使用假的 Whisper 模型覆盖逐词时间戳处理，不访问网络也不加载真实模型。         一个 segment 同时包含标点断句和末尾无标点文本，可验证两 (+2 more)

### Community 28 - "Schema Models & Material Service"
Cohesion: 0.25
Nodes (18): MaterialInfo, VideoAspect, VideoConcatMode, download_videos(), _download_videos_by_script_order(), get_api_key(), _get_tls_verify(), ComfyUI local video-generation provider.      Talks to a minimal OpenAPI-style s (+10 more)

### Community 29 - "Video Transition Tests"
Cohesion: 0.14
Nodes (10): VideoTransitionMode, _detail_frame(), _gradient_clip(), 创建非均匀渐变画面，确保缩放前后的像素差异可以被可靠检测。, 创建包含高频细节的 RGB 帧，用于观察亚像素缩放是否连续响应。, 淡入淡出必须把调用方传入的时长原样交给 MoviePy effect。, 滑入动画的四个方向、结束位置和未知方向兜底都应保持稳定。, 滑出应在片段尾部才开始运动；四个方向、超过结束时间和零时长参数         都需要被夹紧，避免出现除零或素材提前离场。 (+2 more)

### Community 30 - "TTS Providers (Chatterbox/ElevenLabs/Gemini/MiMo)"
Cohesion: 0.18
Nodes (20): chatterbox_tts(), _configure_pydub_ffmpeg(), elevenlabs_tts(), ensure_file_path_exists(), ensure_legacy_submaker_fields(), gemini_tts(), get_audio_duration(), _get_audio_duration_from_submaker() (+12 more)

### Community 31 - "Config & LLM Provider Models"
Cohesion: 0.12
Nodes (16): 原子保存运行时配置。      Streamlit 的不同会话可能在相近时间触发配置保存。直接覆盖 config.toml 时，     另一个线程可能读取到只, save_config(), get_llm_provider(), LLMProviderField, normalize_provider_override(), 只保留与 Registry 默认值不同的用户覆盖值。      WebUI 需要把默认值展示在输入框中，但不能因此把默认值固化到 config.toml；, 描述 Provider 除 API Key、Base URL、模型名之外的额外配置字段。, get_groq_model_ids() (+8 more)

### Community 32 - "Voice Provider Detection"
Cohesion: 0.19
Nodes (19): get_mimo_voices(), is_azure_v2_voice(), is_chatterbox_voice(), is_elevenlabs_voice(), is_gemini_voice(), is_mimo_voice(), is_no_voice(), is_siliconflow_voice() (+11 more)

### Community 33 - "Video Combine/FFmpeg"
Cohesion: 0.14
Nodes (18): combine_videos(), concat_video_clips_with_ffmpeg(), delete_files(), _disable_runtime_video_codec(), _fallback_write_videofile(), _ffmpeg_encoder_exists(), _get_configured_video_codec(), _get_effective_video_codec() (+10 more)

### Community 34 - "LLM Provider Tests"
Cohesion: 0.11
Nodes (5): Azure OpenAI 的鉴权、endpoint 和 api-version 都由 AzureOpenAI 客户端处理。         这个测试覆盖 iss, 默认值只用于运行和展示，只有不同值才应写入用户配置。, Gemini 适配器应通过新版 SDK 的统一 Client 发起内容生成请求。, VolcEngine Ark 暴露 OpenAI-compatible Chat Completions。         这里用 fake OpenAI cl, TestLiteLLMProvider

### Community 35 - "Video Tests"
Cohesion: 0.12
Nodes (7): _FakeMoviePyClip, BGM 打开失败时仍应只写一次无 BGM 视频，并返回 False。, 0 音量必须在解析文件前统一短路当前来源和未来提供商。, 默认曲库需要循环，任务层提供的时长适配文件不应依赖提供商名称。, 为最终混音单测提供最小 MoviePy 接口，避免 CI 真实编码大型视频。, MoviePy 2.1.x 的 FFMPEG_VideoReader 会直接向 stdout 打印 metadata         和 ffmpeg 命令。项, BGM 混合成功后应返回 True，并释放所有原始文件 reader。

### Community 36 - "Config Module"
Cohesion: 0.15
Nodes (10): _can_resolve_hostname(), _decode_linux_route_gateway(), get_container_default_gateway_ip(), get_default_ollama_base_url(), is_running_in_container(), 读取 Linux 容器里的默认网关 IP。      Docker Desktop 通常提供 `host.docker.internal`，但原生 Linux, 返回 Ollama 的默认 OpenAI-compatible base_url。      用户显式配置 `ollama_base_url` 时不会走这里；这, 判断当前进程是否运行在容器内。      这个判断主要用于 Ollama 默认地址选择：     - 普通本机运行时，`localhost` 指向用户机器本身； (+2 more)

### Community 37 - "Video Service Tests"
Cohesion: 0.12
Nodes (7): local 素材路径来自 API 参数，不能允许任意绝对路径进入 MoviePy。         这里验证非 local_videos 白名单目录内的路径会被, BGM 列表接口现在只暴露文件名；生成视频时应能把文件名安全解析回         resource/songs 白名单目录，保持正常使用路径可用。, 用户选择的硬件编码器必须先经过 FFmpeg encoder 列表检测。检测不到         时直接回退 libx264，避免生成任务在写文件阶段才失败。, 如果 libx264 兜底也失败，失败原因更可能是输出路径、权限、文件占用等         通用问题，不能误判为硬件编码器不可用。, 随机模式下，一个长素材会被拆成多个片段。调度层应先让每个源素材         至少出现一次，再使用同一源素材的其他切片，降低用户感知到的重复。, 顺序模式本身只取每个素材的首段，不应被随机调度逻辑改变顺序。, TestVideoService

### Community 38 - "Project Docs & AI Agent"
Cohesion: 0.13
Nodes (16): AI Agent Workflow, CLI (cli.py), Configuration (config.toml / config.example.toml), Deployment Options (Docker, uv, Google Colab, Windows One-Click), AI Agent Skill (SKILL.md), SKILL.md (Skill Definition for AI Agents), Agent Exit Codes (0=success, 10=needs_credentials, 1=error), MoneyPrinterTurbo (AI Short Video Generator) (+8 more)

### Community 39 - "ASGI App & Ping"
Cohesion: 0.18
Nodes (13): application_lifespan(), exception_handler(), get_application(), Request, Application implementation - ASGI., 集中处理 API 进程启动恢复和关闭日志。, Initialize FastAPI application.      Returns:        FastAPI: Application object, validation_exception_handler() (+5 more)

### Community 41 - "LLM Script Prompt Tests"
Cohesion: 0.12
Nodes (8): 按文案顺序匹配素材依赖 LLM 返回有序关键词。这里不调用真实模型，         只验证服务层会把“按脚本叙事顺序输出”的约束写入 prompt，避免, Provider 错误必须保持 generate_terms 的 List[str] 返回契约。          非空的 ``Error: ...`` 字符串, reasoning 模型可能返回 `<think>...</think>`。脚本生成链路必须只保留         最终正文，避免思考过程进入字幕和配音。, 如果模型只返回思考块而没有最终答案，应视为空内容，触发重试或明确错误。, 某些网关可能因为截断只返回未闭合的 `<think>`。这种内容同样不能         进入最终脚本；如果清理后没有正文，就应该按空响应处理。, 高级文案要求只作为附加约束，不替换默认系统提示词。         这样普通用户不配置时仍然走稳定默认规则，高级用户也能细化风格。, 自定义 system prompt 会替换默认脚本规则，但视频主题、语言、段落数         仍由服务层统一追加，避免高级用户漏写必要上下文。, TestScriptPromptOptions

### Community 42 - "Redis Task Manager Tests"
Cohesion: 0.14
Nodes (5): RedisTaskManager, Redis 只能存 JSON；VideoParams 应转换成字典，但原任务仍需保留模型，         避免序列化副作用影响日志、重试或调用方后续读取。, 从 Redis 取出的任务应恢复可调用函数和 VideoParams 模型。, 队列判空和长度必须直接反映 Redis 当前列表长度。, TestRedisTaskManager

### Community 43 - "Controller Base Tests"
Cohesion: 0.18
Nodes (6): new_router(), 客户端提供 request ID 时需要原样保留，缺失时则生成可记录到日志和         错误响应中的 UUID，保证两种入口都有可追踪标识。, 配置了 API Key 时，相同请求头必须正常通过鉴权。, 缺失和错误的 API Key 都必须返回 401，并保留客户端 request ID，         避免鉴权失败在日志中无法与调用方请求对应。, 所有 V1 路由都应复用统一前缀，并仅在传入时设置鉴权依赖。, TestControllerAuthentication

### Community 44 - "External Dependencies"
Cohesion: 0.15
Nodes (14): azure-cognitiveservices-speech (Azure TTS), Background Music (resource/songs), Batch Video Generation, Edge TTS Voice List, edge_tts (TTS Provider), Edge TTS Voices (940+ voices, multilingual), faster-whisper (ASR), Multilingual Video Script Generation (+6 more)

### Community 45 - "Controller Video Helper Tests"
Cohesion: 0.14
Nodes (7): 非法 Range 必须返回 416，不能因 split 或 int 转换异常变成 500。, Windows 和 POSIX 客户端路径都只能保留最后一段安全文件名。, API 进程启动时必须执行一次发布遗留状态恢复。, 空文件名和目录占位符不能进入服务端存储路径。, 不存在文件返回 404，目录穿越等非法路径返回 403。, 播放器常见的闭区间、开放区间和后缀区间都应得到准确边界。, TestVideoControllerHelpers

### Community 46 - "Subtitle Background Tests"
Cohesion: 0.14
Nodes (6): 新任务和独立字幕接口都不应在用户未指定时渲染字幕背景。, 中文长句按字符换行时，句号等闭合标点不能独占一行，否则字幕背景         会被一个单独的小点撑高。这里复现大字号中文长句的边界情况。, WebUI 新增字幕背景开关和颜色选择器后，所有已有语言都必须包含对应         翻译 key，避免某些语言界面直接显示英文内部 key。, UI 会根据开关向后端传递 False 或颜色字符串。这里验证 schema 仍然         接受这两种值，避免后续依赖或类型调整破坏 WebUI 与合成, TextClip 的画布会包含字体行高和 baseline 空白，直接居中画布会让         字幕在背景里看起来偏下。这里用一个假 mask 模拟“可见文, TestSubtitleBackgroundSettings

### Community 48 - "Voice Service Tests"
Cohesion: 0.14
Nodes (3): 验证 Gemini TTS 返回的 legacy 字幕结构在 edge provider 下可以直接产出         SRT，不会因为匹配失败而回退到 Wh, Edge TTS 会把 "1,000 years" 作为连续文本返回。脚本断句时不能把         数字中间的英文逗号当成句子边界，否则字幕聚合会出现 is, TestVoiceService

### Community 49 - "WebUI i18n Tests"
Cohesion: 0.21
Nodes (3): _load_translation(), TestWebuiI18n, _TrKeyVisitor

### Community 51 - "TwelveLabs Service"
Cohesion: 0.26
Nodes (12): analyze_clip(), _client(), _cosine(), embed_text(), _embed_text_cached(), is_enabled(), TwelveLabs (https://twelvelabs.io) integration — optional, opt-in helpers.  This, Reorder `search_terms` so the terms most semantically relevant to     `video_sub (+4 more)

### Community 52 - "Video Effects Utils"
Cohesion: 0.22
Nodes (12): fadein_transition(), fadeout_transition(), 在整个片段内从原始画面平滑放大到 1.2 倍。, 在整个片段内从 1.2 倍平滑缩小到原始画面。, 使用亚像素中心裁剪实现无黑边且稳定的缩放效果。      不能先把裁剪宽高转换为整数：缩放比例连续变化时，整数边界会按不同步长跳动，     并在奇偶尺寸切换时, slidein_transition(), slideout_transition(), _zoom_frame() (+4 more)

### Community 54 - "TwelveLabs Tests"
Cohesion: 0.18
Nodes (3): TwelveLabs 集成是完全 opt-in 的：未配置 twelvelabs_api_keys 时所有函数     都必须是无副作用的 no-op，行为与不, Build a fake TwelveLabs client whose embed.create returns canned vectors., TestTwelveLabsService

### Community 55 - "WebUI Task History Tests"
Cohesion: 0.15
Nodes (10): _load_task_history_helpers(), 恢复上传配音任务时，继续使用上传模式必须重新选择音频文件。, 用户主动切换到自动配音或无配音时，不再强制恢复历史上传文件。, 从 WebUI 入口中隔离加载不依赖 Streamlit 的任务历史纯函数。      直接导入 Main.py 会执行整套页面渲染。测试只编译目标常量和函数，, 任务历史只能把 final 成片识别为完成，不能使用合成中间文件。, 多成片任务与运行时结果保持一致，默认播放序号最小的最终视频。, test_find_final_task_video_ignores_intermediate_files(), test_find_final_task_video_returns_first_numbered_output() (+2 more)

### Community 56 - "LLM Gateway & Dependencies"
Cohesion: 0.23
Nodes (12): API (FastAPI), dashscope (Qwen SDK), fastapi (API Framework), google-genai (Gemini SDK), litellm (LLM Gateway), LLM Gateways (Cloudflare, ModelScope, AIHubMix, AIML, EvoLink, Ollama, OneAPI, LiteLLM, Groq, Pollinations), LLM Providers (Kimi, OpenAI, Gemini, DeepSeek, Qwen, Azure, VolcEngine, Grok, MiniMax, MiMo), loguru (Logging) (+4 more)

### Community 57 - "Config Persistence Tests"
Cohesion: 0.21
Nodes (6): 示例配置应展示用户需要手工维护的服务、素材和高级运行参数。, Registry 中可配置的 Provider 字段必须能在示例文件中被发现。, 发布配置必须位于 app 节点，确保示例文件与运行时读取路径一致。, 配置保存先写临时文件再原子替换。测试同时确认输出仍是合法 TOML，         且成功保存后不会在配置目录遗留临时文件。, 长任务持有运行锁时，其它会话不能在任务中途改写全局配置。, TestConfigPersistence

### Community 58 - "LLM Connection Tests"
Cohesion: 0.17
Nodes (5): 连接测试只发送一次固定最小请求，不触发脚本生成重试。, Provider 返回错误时应保留可诊断信息，并报告本次请求耗时。, 极端情况下的空响应应显示明确错误，而不是误报连接成功。, TestLiteLLMLiveIntegration, TestLLMConnection

### Community 59 - "WebUI Fonts & Task Restore"
Cohesion: 0.22
Nodes (11): font_dir(), _apply_pending_task_restore(), _build_restore_upload_requirements(), get_all_fonts(), 恢复 WebUI 字幕控件和持久化配置中的默认值。, 记录历史任务中无法由 Streamlit 自动恢复的上传文件依赖。      浏览器不允许程序重新填充 file_uploader，因此恢复任务时需要单独记录本, 按固定顺序渲染顶部栏、弹窗、生成表单和任务结果。, _render_application() (+3 more)

### Community 60 - "Sponsor SVG (PicWish)"
Cohesion: 0.22
Nodes (10): #52B4FE, #5555FF, #85E7FE, sponsors, PicWish Logo SVG, Path #1, Path #2, Path #3 (+2 more)

### Community 61 - "Video Schema & LLM Controller Tests"
Cohesion: 0.24
Nodes (6): {       "video_subject": "春天的花海",       "video_language": "",       "paragraph_n, VideoScriptParams, VideoScriptRequest, 素材顺序匹配开关必须继续传递到关键词生成服务。, TestLlmController, API 请求模型需要限制高级 prompt 参数，避免外部调用绕过 WebUI         传入异常段落数或超长提示词，导致模型成本和结果不可控。

### Community 62 - "Azure TTS v2 & Subtitle Formatter"
Cohesion: 0.22
Nodes (10): azure_tts_v2(), _build_azure_v2_ssml(), create_subtitle(), _do(), _format_text(), 清理字幕对齐前的脚本文本。      这里不能只在 LLM 生成阶段处理，因为用户也可能手动粘贴脚本，或通过     API 直接传入包含 Markdown 标, 将已经聚合好的字幕段写入到 SRT 文件，并做一次基本可读性验证。      返回值：     - `True`：字幕文件成功落盘且可被 moviepy 解析；, 优化字幕文件     1. 将字幕文件按照标点符号分割成多行     2. 逐行匹配字幕文件中的文本     3. 生成新的字幕文件 (+2 more)

### Community 63 - "Subtitle Item Builders"
Cohesion: 0.22
Nodes (10): _build_subtitle_formatter(), _build_subtitle_items_from_edge_cues(), _build_subtitle_items_from_legacy_submaker(), _match_script_line(), _normalize_arabic(), 返回统一的 SRT 行格式化函数。      这里单独拆成一个小工具，是为了让 edge_tts 7.x 的 cues 路径     和项目原有的 legacy, 统一阿拉伯语常见字母变体，提升字幕 cue 与脚本行的匹配容错率。      edge-tts 对阿拉伯语可能返回与原脚本不同的字母形态，例如把 أ/إ/آ, 尝试把当前累计的字幕文本，与脚本中的某一条标准断句匹配起来。      这里复用了项目原有的“按标点拆脚本，再逐段比对”的思路：     1. 优先精确匹配； (+2 more)

### Community 64 - "Docker Compose & Dockerfile"
Cohesion: 0.20
Nodes (9): Docker Compose Shared Volumes (code mount), Docker Compose Services: webui (8501), api (8080), Docker Compose (Local Dev), Dockerfile Installs: ffmpeg, git, Dockerfile Mirror Support (Aliyun, Tsinghua, Default), Dockerfile Pip Mirror Support (Aliyun, Tsinghua, Official), Dockerfile Base: Python 3.11-slim-bullseye, Dockerfile CMD: streamlit run webui/Main.py (+1 more)

### Community 65 - "Sponsor SVG (RecCloud)"
Cohesion: 0.33
Nodes (9): Accent Shape (Light Green #69F7C4), Clip Path (clip0_10790_997), Group with Clip Path, Inner Circle (Green #18AD25), Middle Ring (White), Outer Circle (Green #12C456), RecCloud, docs/sponsors Directory (+1 more)

### Community 66 - "Ollama Provider Tests"
Cohesion: 0.27
Nodes (4): 普通本机运行时，Ollama 默认仍然使用 localhost，避免影响已有用户。, 容器内运行时，localhost 指向容器自身；默认改为 host.docker.internal，         方便 Docker Desktop 用户访, 原生 Linux Docker 里不一定能解析 host.docker.internal。此时使用容器         默认网关作为兜底地址，比直接返回不可解析, 用户手动配置的 ollama_base_url 优先级最高，不受容器检测影响。

### Community 67 - "Qwen Provider Tests"
Cohesion: 0.27
Nodes (4): DashScope chat 模式会把文本放在 `output.choices[0].message.content`。         这里覆盖 issue, 保留旧 DashScope completion 响应结构的兼容路径。, Qwen 空响应应返回可诊断错误，而不是底层 AttributeError。, Qwen chat 响应 choices 为空时应返回明确错误。

### Community 68 - "LLM Provider Spec"
Cohesion: 0.22
Nodes (4): LLMProviderSpec, LLM Provider 的集中声明。      这里集中保存跨 WebUI、配置加载和服务调用都会使用的稳定元数据，包括默认     展示名称和 locale, 将空值或已废弃的历史默认值统一解析为当前默认模型。, 解析 Base URL，并将已经停用的历史地址迁移到当前默认值。

### Community 69 - "GitHub CI/CD & Redis"
Cohesion: 0.22
Nodes (9): Cross-Platform Publishing (TikTok, Instagram, YouTube Shorts via Upload-Post), CI Workflow, CI Pytest with Coverage, CI Python Versions (3.11, 3.13), CI Redis Service (redis:7-alpine), CI Ruff Linter, CI uv Package Manager, CI Windows Smoke Tests (+1 more)

### Community 70 - "WebUI Segmented Controls"
Cohesion: 0.28
Nodes (9): localized_widget_key(), 在文案顺序匹配开启时固定使用顺序拼接，并在关闭后恢复原选择。, 使用稳定业务值创建单选分段控件，避免语言切换后状态被展示文案覆盖。, 渲染背景音乐来源与音量设置，并返回本次待保存的上传文件。, _render_background_music_settings(), _render_video_settings(), stable_segmented_control(), stable_selectbox() (+1 more)

### Community 71 - "Video Social Metadata"
Cohesion: 0.25
Nodes (5): {       "video_subject": "A day in Shanghai",       "video_script": "",       "l, VideoSocialMetadataParams, VideoSocialMetadataRequest, 社交平台元数据接口应保持服务层结果的响应结构。, 外部 API 不能接受无限长的脚本和语言参数，否则会直接放大 LLM         token 成本。schema 层先拦截，服务层再做内部调用兜底。

### Community 72 - "LLM Tutorial Transcripts"
Cohesion: 0.43
Nodes (8): LLM Tutorial Video Concept, LLM Tutorial Video, LLM Tutorial Video, LLM Tutorial Video, LLM Tutorial Video, LLM Tutorial Video, LLM Tutorial Video, LLM Tutorial Video

### Community 73 - "SynchronizedConfig Dict Ops"
Cohesion: 0.29
Nodes (3): 保持 dict 使用方式不变，同时让运行期配置写操作服从同一把锁。, _SynchronizedConfig, dict

### Community 74 - "WebUI Script Settings"
Cohesion: 0.29
Nodes (7): 在一次依赖全局配置的完整操作期间阻止其它 WebUI 会话改写配置。      当前项目默认绑定本地回环地址，配置仍然是单用户全局配置。这个轻量锁主要, runtime_config_lock(), 将高级脚本设置中的系统提示词恢复为当前版本的默认内容。, 展示将要发送给大模型的完整脚本生成提示词。, render_script_prompt_preview(), _render_script_settings(), reset_script_system_prompt()

### Community 79 - "WebUI Task Restore"
Cohesion: 0.29
Nodes (7): _find_final_task_video(), _format_task_subject(), _load_task_restore_payload(), 返回任务目录中序号最小的最终成片。      合成流程还会产生 combined、temp-clip 和 MoviePy 临时文件，这些文件不能     表示任, _render_task_restore_dialog(), _safe_load_task_script(), _scan_history_tasks()

### Community 80 - "GitHub Issue Templates"
Cohesion: 0.33
Nodes (6): Blank Issues Disabled (config.yml), Bug Report Template, Bug Report Template (Bilingual EN/ZH), Blank Issues Disabled Config, Feature Request Template, Feature Request Template (Bilingual EN/ZH)

### Community 81 - "Docker Release & Publish"
Cohesion: 0.33
Nodes (6): Docker Compose Release Volumes (config.toml, storage), Docker Compose Release (Prebuilt GHCR Image), Docker Compose Release (Prebuilt Images), Docker BuildKit Cache (GH Actions), Docker Publish to GHCR (Multi-platform amd64/arm64), Docker Publish Workflow (GHCR)

### Community 82 - "Transcript Placeholders"
Cohesion: 0.33
Nodes (6): Transcript output005, Transcript output008, Transcript output015, Transcript output017, Transcript output021, Transcript Placeholder Content (tutorial.com, LLM references)

### Community 83 - "LLM Video Concepts"
Cohesion: 0.40
Nodes (6): LLM (Large Language Model), Video about how to use LLMs, Video tutorial about using LLMs, LLM (Large Language Model), Video about how to use LLMs, Video tutorial about using LLMs

### Community 84 - "Video Combine Speed Tests"
Cohesion: 0.33
Nodes (3): 使用轻量假视频记录 combine_videos 实际读取的源时间范围。, 0.5 倍慢放应连续读取 1.5 秒源片段，不能跳过中间画面。, 2 倍快放应读取 6 秒源画面，使最终片段仍保持 3 秒。

### Community 86 - "Video SubclippedClip"
Cohesion: 0.40
Nodes (3): _prioritize_unique_source_clips(), 优先让每个源素材只出现一次，降低成片里同一素材反复出现的概率。      线上素材经常会遇到“一个长视频被切成多个短片段”的情况。旧逻辑在     random, SubClippedVideoClip

### Community 87 - "Create Project Tutorials"
Cohesion: 0.70
Nodes (5): Create New Project Tutorial Concept, Create New Project Tutorial, Create New Project Tutorial, Create New Project Tutorial, Create New Project Tutorial

### Community 88 - "Tutorial Website References"
Cohesion: 0.60
Nodes (5): Tutorial Website Reference, www.tutorial.com, www.tutorial.com, www.tutorial.com, www.tutorial.com

### Community 89 - "Test Structure & Coverage"
Cohesion: 0.40
Nodes (5): Test Coverage: pytest-cov, Integration Tests: MPT_RUN_INTEGRATION_TESTS=1, Test Framework: pytest + unittest.TestCase compatibility, Test Directory Documentation, Test Structure: services/ (domain-focused unit tests)

### Community 90 - "AGENTS.md Graphify"
Cohesion: 0.50
Nodes (4): Graphify Agent Instructions, Graphify Knowledge Graph (graphify-out/), Graphify Commands (query, path, explain), graphify update (AST-only graph refresh)

### Community 91 - "Subtitle Font Support"
Cohesion: 0.50
Nodes (4): 检查字体是否包含样本文字需要的字形，并缓存重复检查结果。, 检查字体能否绘制文本中的字母和数字，忽略空白及标点符号。, _subtitle_font_supports_sample(), subtitle_font_supports_text()

### Community 92 - "OpenCode Plugin Graphify"
Cohesion: 0.50
Nodes (3): plugin, $schema, .opencode/plugins/graphify.js

### Community 94 - "YouTube Outro Next Video"
Cohesion: 1.00
Nodes (3): YouTube Outro Next Video Pattern, YouTube Outro - Subscribe and Next Video, YouTube Outro - Thanks and Next Video

### Community 95 - "YouTube Outro Subscribe"
Cohesion: 1.00
Nodes (3): YouTube Outro Subscribe Pattern, YouTube Outro - Subscribe Like Share, YouTube Outro - Subscribe Like Bell

### Community 96 - "BytePlus Sponsor"
Cohesion: 1.00
Nodes (3): BytePlus Brand, BytePlus Logo SVG, MoneyPrinterTurbo Sponsor: BytePlus

### Community 97 - "GitHub Security Policy"
Cohesion: 0.67
Nodes (3): Security Policy: Private Vulnerability Reporting (GitHub), Security Policy: Supported Versions (main branch + latest release), Security Policy

## Ambiguous Edges - Review These
- `Video Generation Pipeline` → `Transcript Placeholder Content (tutorial.com, LLM references)`  [AMBIGUOUS]
  graphify-out/transcripts/output005.txt · relation: sample_output_of

## Knowledge Gaps
- **68 isolated node(s):** `$schema`, `.opencode/plugins/graphify.js`, `_Config`, `moneyprinterturbo`, `webui.sh script` (+63 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **83 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Video Generation Pipeline` and `Transcript Placeholder Content (tutorial.com, LLM references)`?**
  _Edge tagged AMBIGUOUS (relation: sample_output_of) - confidence is low._
- **Why does `MaterialInfo` connect `Schema Models & Material Service` to `Video Pipeline Core`, `TTS Tests`, `Video Tests`, `Subtitle Service`, `Video Service Tests`, `LLM Provider Tests`, `Video Material Resolution Tests`, `CLI Interface`, `Video SubclippedClip`, `Video Service Core`, `WebUI Main App`?**
  _High betweenness centrality (0.111) - this node is a cross-community bridge._
- **Why does `VideoParams` connect `Video Pipeline Core` to `Video Pipeline Tests`, `Subtitle Service`, `LLM Provider Models`, `LLM Provider Tests`, `Redis Task Manager Tests`, `Task Manager Base/Memory`, `Subtitle Background Tests`, `Video Controller v1`, `CLI Interface`, `Video SubclippedClip`, `Video Service Core`, `WebUI Main App`, `WebUI Fonts & Task Restore`?**
  _High betweenness centrality (0.082) - this node is a cross-community bridge._
- **Why does `TestVideoService` connect `Video Service Tests` to `BGM Path Security`, `FFmpeg Binary Env Path`, `FFmpeg Fallback`, `Video Codec Default`, `Video Codec Preserve`, `FFmpeg Encoder Fallback`, `VideoFile Fallback`, `FFmpeg Concat Path Normalize`, `Concat Fallback`, `Concat Codec Fallback`, `Combine Videos Audio Duration`, `Transition Mode None`, `Combine Videos Duration Margin`, `Concat Audio Duration Limit`, `Unique Source Clips`, `Wrap Text Test`, `Rounded Subtitle Background`, `Schema Models & Material Service`, `Video Tests`, `Video Material Resolution Tests`, `Video Combine Speed Tests`, `BGM Project Relative Path`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `VideoParams` (e.g. with `RedisTaskManager` and `.enqueue()`) actually correct?**
  _`VideoParams` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `TestLiteLLMProvider` (e.g. with `VideoScriptRequest` and `VideoSocialMetadataRequest`) actually correct?**
  _`TestLiteLLMProvider` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `TestTaskService` (e.g. with `MaterialInfo` and `VideoParams`) actually correct?**
  _`TestTaskService` has 4 INFERRED edges - model-reasoned connections that need verification._