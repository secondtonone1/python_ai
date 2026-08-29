-- =============================================================
-- SmartService AI 智能客服系统 数据库初始化脚本
-- 执行方式:
--   1) Navicat 中直接打开本文件执行
--   2) 命令行: mysql -h主机 -P端口 -u用户 -p < init_db.sql
-- =============================================================

CREATE DATABASE IF NOT EXISTS ai_service_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

USE ai_service_db;

-- ---------------------------------------------------------------
-- 客服账号表 (密码存储: SHA256(盐 + 明文) 哈希, 不存明文)
-- 预置账号: admin / 123456
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS t_staff (
    id            BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
    username      VARCHAR(64)  NOT NULL UNIQUE      COMMENT '登录名',
    password_hash CHAR(64)     NOT NULL             COMMENT 'SHA256(盐+密码)',
    display_name  VARCHAR(64)  NOT NULL DEFAULT ''  COMMENT '显示名称',
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE = InnoDB COMMENT = '客服账号表';

INSERT INTO t_staff (username, password_hash, display_name)
VALUES ('admin', '5f5ca6ffd025d7eb46a22df4a1551e523b39412ce9615d3e6c1389c51db2fb2f', '值班客服')
ON DUPLICATE KEY UPDATE display_name = VALUES(display_name);

-- ---------------------------------------------------------------
-- 会话表 (一次访客咨询 = 一个会话)
-- 状态机: bot(机器人接待) -> waiting_human(待人工) -> human(人工中)
--         -> closed(已关闭) / archived(超时归档)
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS t_session (
    id           BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
    visitor_name VARCHAR(64)  NOT NULL DEFAULT '访客' COMMENT '访客昵称',
    status       VARCHAR(20)  NOT NULL DEFAULT 'bot'  COMMENT '会话状态',
    created_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
                 ON UPDATE CURRENT_TIMESTAMP COMMENT '最后活动时间',
    closed_at    DATETIME     DEFAULT NULL COMMENT '关闭时间',
    KEY idx_status (status),
    KEY idx_updated (updated_at)
) ENGINE = InnoDB COMMENT = '客服会话表';

-- ---------------------------------------------------------------
-- 消息表 (用户/机器人/客服 三方消息都存这里)
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS t_message (
    id         BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
    session_id BIGINT       NOT NULL                COMMENT '所属会话',
    role       VARCHAR(10)  NOT NULL                COMMENT '角色: user/bot/staff',
    content    TEXT         NOT NULL                COMMENT '消息内容',
    source     VARCHAR(20)  DEFAULT NULL            COMMENT '机器人回答来源: knowledge/pending/fallback/human',
    rating     TINYINT      DEFAULT NULL            COMMENT '满意度: 1满意 -1不满意 NULL未评价',
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '发送时间',
    KEY idx_session_id (session_id, id)
) ENGINE = InnoDB COMMENT = '会话消息表';

-- ---------------------------------------------------------------
-- 知识库表 (规则引擎的数据源; 后续阶段可升级为向量检索/RAG)
-- keywords 使用逗号分隔多个关键词, 命中任一关键词即得分
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS t_knowledge (
    id         BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
    category   VARCHAR(64)  NOT NULL DEFAULT '' COMMENT '分类',
    question   VARCHAR(255) NOT NULL                COMMENT '标准问题',
    keywords   VARCHAR(255) NOT NULL                COMMENT '关键词(逗号分隔)',
    answer     TEXT         NOT NULL                COMMENT '标准答案',
    enabled    TINYINT      NOT NULL DEFAULT 1      COMMENT '是否启用: 1启用 0停用',
    hit_count  INT          NOT NULL DEFAULT 0      COMMENT '命中次数(运营数据)',
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    KEY idx_enabled (enabled)
) ENGINE = InnoDB COMMENT = '客服知识库表';

-- ---------------------------------------------------------------
-- 演示知识库 (培训机构客服场景)
-- ---------------------------------------------------------------
INSERT INTO t_knowledge (category, question, keywords, answer) VALUES
('课程', '你们都有哪些课程', '课程,有哪些课,学什么,课程体系', '我们开设四大课程体系：\n1. Python 基础与进阶（面向零基础）\n2. Dify 低代码 AI 应用开发\n3. 机器学习与深度学习\n4. LangChain / LangGraph 大模型应用开发\n回复序号可以了解详情。'),
('课程', 'Python课程适合零基础吗', '零基础,没基础,小白,入门', '完全可以！Python 基础阶段从变量、循环、函数讲起，配有大量课堂案例和课后作业，零基础学员也能跟上。'),
('课程', '课程怎么收费', '学费,价格,多少钱,费用,收费', '不同阶段收费标准不同：Python 基础+进阶阶段学费 6980 元，AI 应用开发（含 Dify、机器学习、LangChain）阶段学费 12800 元。两阶段连报可享 9 折优惠。'),
('课程', '什么时候开班', '开班,什么时候,上课时间,开班时间', '每月 1 号和 15 号滚动开班。晚班 19:00-21:30（周二/四/六），周末班 9:30-17:30。最新班期请咨询人工客服确认。'),
('课程', '上课方式是什么', '上课方式,直播,录播,线上,线下', '采用线上直播 + 录播回放 + 课后答疑的上课方式，直播有互动答疑环节，错过直播可无限次看回放。'),
('课程', '怎么报名', '报名,怎么报名,如何报名,联系', '报名流程：\n1. 联系客服预约试听\n2. 试听后确定班期\n3. 缴纳定金锁定名额\n4. 开班前补齐学费\n现在回复"转人工"即可联系报名老师。'),
('课程', '学习资料怎么获取', '资料,课件,代码,笔记,素材', '每节课的课件、源码和笔记会在课后上传到班级资料库，学员可随时下载；项目实战阶段的完整代码仓库也会同步开放。'),
('课程', '学完能就业吗', '就业,找工作,前景,工资', '课程对标企业真实项目（本项目就是教学案例之一），学完可胜任 Python 开发、AI 应用开发等岗位。我们与 30+ 合作企业建立人才推荐通道，往期学员就业率 92%。');
