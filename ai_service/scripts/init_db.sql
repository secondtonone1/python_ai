-- =============================================================
-- 心聆 MindEcho 在线心理支持平台 数据库初始化脚本
-- 执行方式:
--   1) Navicat 中直接打开本文件执行
--   2) 命令行: mysql -h主机 -P端口 -u用户 -p < init_db.sql
-- =============================================================

CREATE DATABASE IF NOT EXISTS ai_service_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

USE ai_service_db;

-- ---------------------------------------------------------------
-- 咨询师账号表 (密码存储: SHA256(盐 + 明文) 哈希, 不存明文)
-- 预置账号: admin / 123456
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS t_staff (
    id            BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
    username      VARCHAR(64)  NOT NULL UNIQUE      COMMENT '登录名',
    password_hash CHAR(64)     NOT NULL             COMMENT 'SHA256(盐+密码)',
    display_name  VARCHAR(64)  NOT NULL DEFAULT ''  COMMENT '显示名称',
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE = InnoDB COMMENT = '咨询师账号表';

INSERT INTO t_staff (username, password_hash, display_name)
VALUES ('admin', '5f5ca6ffd025d7eb46a22df4a1551e523b39412ce9615d3e6c1389c51db2fb2f', '在线咨询师')
ON DUPLICATE KEY UPDATE display_name = VALUES(display_name);

-- ---------------------------------------------------------------
-- 会话表 (一次来访 = 一个会话)
-- 状态机: bot(心理助手接待) -> waiting_human(待接入) -> human(咨询师接待中)
--         -> closed(已结束) / archived(超时归档)
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS t_session (
    id           BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
    visitor_name VARCHAR(64)  NOT NULL DEFAULT '来访者' COMMENT '来访者昵称',
    status       VARCHAR(20)  NOT NULL DEFAULT 'bot'  COMMENT '会话状态',
    created_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
                 ON UPDATE CURRENT_TIMESTAMP COMMENT '最后活动时间',
    closed_at    DATETIME     DEFAULT NULL COMMENT '关闭时间',
    KEY idx_status (status),
    KEY idx_updated (updated_at)
) ENGINE = InnoDB COMMENT = '咨询会话表';

-- ---------------------------------------------------------------
-- 消息表 (来访者/心理助手/咨询师 三方消息都存这里)
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS t_message (
    id         BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
    session_id BIGINT       NOT NULL                COMMENT '所属会话',
    role       VARCHAR(10)  NOT NULL                COMMENT '角色: user/bot/staff',
    content    TEXT         NOT NULL                COMMENT '消息内容',
    source     VARCHAR(20)  DEFAULT NULL            COMMENT '回答来源: knowledge/pending/fallback/human',
    rating     TINYINT      DEFAULT NULL            COMMENT '满意度: 1满意 -1不满意 NULL未评价',
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '发送时间',
    KEY idx_session_id (session_id, id)
) ENGINE = InnoDB COMMENT = '会话消息表';

-- ---------------------------------------------------------------
-- 知识库表 (心理助手规则引擎的数据源; 后续阶段可升级为向量检索/RAG)
-- keywords 使用逗号分隔多个关键词, 命中任一关键词即得分
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS t_knowledge (
    id         BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
    category   VARCHAR(64)  NOT NULL DEFAULT '' COMMENT '分类',
    question   VARCHAR(255) NOT NULL                COMMENT '标准问题',
    keywords   VARCHAR(255) NOT NULL                COMMENT '关键词(逗号分隔)',
    answer     TEXT         NOT NULL                COMMENT '标准回答',
    enabled    TINYINT      NOT NULL DEFAULT 1      COMMENT '是否启用: 1启用 0停用',
    hit_count  INT          NOT NULL DEFAULT 0      COMMENT '命中次数(运营数据)',
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    KEY idx_enabled (enabled)
) ENGINE = InnoDB COMMENT = '心理支持知识库表';

-- ---------------------------------------------------------------
-- 演示知识库 (心聆在线心理支持场景; 仅教学演示, 不构成医疗/心理诊断)
-- ---------------------------------------------------------------
INSERT INTO t_knowledge (category, question, keywords, answer) VALUES
('情绪困扰', '总是很焦虑、静不下来怎么办', '焦虑,紧张,坐立不安,心慌,担心,怕', '适度的焦虑是正常的“警报系统”，当它反复出现时，可以试试：\n1. 4-7-8 呼吸：吸气 4 秒 → 屏住 7 秒 → 呼气 8 秒，重复 4 轮，让身体慢下来；\n2. 把“最坏的结果”写下来，再在旁边写下“最可能的结果”，让担忧变得具体；\n3. 每天留 20 分钟散步或拉伸，把多余的紧张代谢掉。\n如果这种状态持续两周以上、明显影响睡眠或学习工作，建议预约咨询师做一次正式评估。'),
('情绪困扰', '情绪低落、提不起劲怎么办', '低落,抑郁,难过,开心不起来,想哭,没意思,不想动', '情绪低落时，先别急着“振作起来”，允许自己慢一点：\n1. 用小到不可能失败的动作启动，比如起床喝一杯温水、出门走 5 分钟；\n2. 保持基本生活节律：按时吃饭、固定入睡时间；\n3. 找一位信任的人说出来，或把感受写下来。\n如果连续两周以上几乎每天都低落、连喜欢的事也提不起兴趣，这值得认真对待，请预约咨询师聊一聊。'),
('睡眠困扰', '晚上睡不着、失眠怎么办', '失眠,睡不着,入睡困难,睡不好,熬夜,多梦,半夜醒', '睡眠是“放松下来自然发生”的过程，越用力越容易醒。可以先做：\n1. 睡前 1 小时关掉短视频，改看纸质书或听轻音乐；\n2. 躺下 20 分钟仍睡不着就起床，去客厅做点无聊的事，困了再回床——让床只和睡觉建立联系；\n3. 白天固定起床时间，午睡不超过 30 分钟。\n若失眠持续一个月以上并影响白天状态，建议让咨询师陪你做睡眠行为分析。'),
('压力管理', '工作或学习压力大怎么调节', '压力,加班,学不动,累,崩溃,喘不过气,任务多', '压力大时，人容易在“硬扛”和“彻底躺平”之间摆动，更可持续的做法是：\n1. 把任务拆成 25 分钟的小块，一次只做一块，完成就休息（番茄钟）；\n2. 主动设置“关机时间”，哪怕只有 20 分钟完全属于自己；\n3. 每天记录三件“已经完成的小事”，对抗大脑只盯着未完成项的习惯。\n若长期高压伴随持续失眠或身体不适，请考虑预约咨询师做压力管理训练。'),
('人际关系', '和人相处很累、害怕社交怎么办', '人际,社交,社恐,合不来,同事,朋友,聚会', '害怕社交往往不是“不会说话”，而是太在意别人的评价。可以慢慢来：\n1. 从低强度社交开始：先约一个朋友吃饭，而不是直接去大型聚会；\n2. 练习把注意力从“我怎么表现”移到“对方在说什么”；\n3. 允许自己安静——关系里本就有沉默的空间。\n如果回避已经影响工作与生活，欢迎预约咨询师，一起看看这份害怕来自哪里。'),
('咨询预约', '怎么预约心理咨询', '预约,咨询,流程,怎么咨询,想咨询', '预约流程很简单：\n1. 在页面发送“转人工”或“预约”，会有咨询师接入你的会话；\n2. 和咨询师说明你想聊的方向与方便的时间；\n3. 由咨询师为你安排正式咨询时段。\n第一次沟通主要是了解情况与建立信任，不用有压力。'),
('咨询预约', '咨询怎么收费、一次多久', '收费,费用,多少钱,价格,时长,多久,贵吗', '平台当前为教学演示，咨询体验不收取费用。正式设置下，单次咨询通常为 50 分钟/次，具体收费与频率由咨询师在首次沟通时和你确认；任何收费安排都会在开始前讲清楚，不会有隐藏费用。'),
('咨询预约', '咨询内容保密吗', '保密,隐私,秘密,会被别人知道吗', '保密是心理咨询的基本原则：谈话内容只保留在你和咨询师之间，不会告知第三方。\n唯一例外是：当你面临伤害自己或他人的现实风险时，为保护你的安全，咨询师有责任联系紧急联系人或救援机构——这恰恰是为了保护你。'),
('咨询预约', '咨询形式是什么样的', '形式,线上,视频,面对面,语音,文字', '平台支持文字与语音两种形式：\n1. 文字：适合先倾诉，节奏由你掌控；\n2. 语音或视频：适合需要即时反馈的深入沟通。\n在会话里告诉咨询师你的偏好即可，她会为你安排合适的形式。'),
('危机求助', '有伤害自己的想法怎么办', '自杀,自伤,轻生,不想活,活着没意思,伤害自己', '听到你这么说，我很心疼，也谢谢你愿意说出来。请你现在先做三件事：\n1. 立刻拨打 120 或 110（身边有人时，请 ta 陪着你）；\n2. 拨打全国心理援助热线 12356（24 小时免费，接通就好，不需要想好说什么）；\n3. 不要独自待着，联系一位你信任的人。\n这种想法是痛苦发出的求救信号，不是你的错——请一定让专业的人陪你现在这一段路。');
