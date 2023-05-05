/*
 Navicat Premium Data Transfer

 Source Server         : mysql5.6
 Source Server Type    : MySQL
 Source Server Version : 50620
 Source Host           : localhost:3306
 Source Schema         : scenic_db

 Target Server Type    : MySQL
 Target Server Version : 50620
 File Encoding         : 65001

 Date: 27/03/2021 17:18:52
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_admin
-- ----------------------------
DROP TABLE IF EXISTS `t_admin`;
CREATE TABLE `t_admin`  (
  `username` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `password` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`username`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_admin
-- ----------------------------
INSERT INTO `t_admin` VALUES ('a', 'a');

-- ----------------------------
-- Table structure for t_leaveword
-- ----------------------------
DROP TABLE IF EXISTS `t_leaveword`;
CREATE TABLE `t_leaveword`  (
  `leaveWordId` int(11) NOT NULL AUTO_INCREMENT COMMENT '留言id',
  `leaveTitle` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '留言标题',
  `leaveContent` varchar(2000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '留言内容',
  `userObj` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '留言人',
  `leaveTime` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '留言时间',
  `replyContent` varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '管理回复',
  `replyTime` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '回复时间',
  PRIMARY KEY (`leaveWordId`) USING BTREE,
  INDEX `userObj`(`userObj`) USING BTREE,
  CONSTRAINT `t_leaveword_ibfk_1` FOREIGN KEY (`userObj`) REFERENCES `t_userinfo` (`user_name`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_leaveword
-- ----------------------------
INSERT INTO `t_leaveword` VALUES (1, '11', '22', 'user1', '2021-03-27 14:27:41', '444', '2021-03-27 14:27:45');
INSERT INTO `t_leaveword` VALUES (2, '3214', 'asfasf', 'user1', '2021-03-27 16:33:41', '--', '--');
INSERT INTO `t_leaveword` VALUES (3, 'bbb', 'cccc', 'user2', '2021-03-27 16:47:21', '--', '--');
INSERT INTO `t_leaveword` VALUES (4, '管理你好，给个建议！', '旅游景点太少了，能多加几个吗？', 'user1', '2021-03-27 17:07:26', '好的，收到', '2021-03-27 17:16:03');

-- ----------------------------
-- Table structure for t_province
-- ----------------------------
DROP TABLE IF EXISTS `t_province`;
CREATE TABLE `t_province`  (
  `provinceId` int(11) NOT NULL AUTO_INCREMENT COMMENT '省份id',
  `provinceName` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '省份名称',
  PRIMARY KEY (`provinceId`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_province
-- ----------------------------
INSERT INTO `t_province` VALUES (1, '四川省');
INSERT INTO `t_province` VALUES (2, '广东省');

-- ----------------------------
-- Table structure for t_scenic
-- ----------------------------
DROP TABLE IF EXISTS `t_scenic`;
CREATE TABLE `t_scenic`  (
  `scenicId` int(11) NOT NULL AUTO_INCREMENT COMMENT '景点id',
  `provinceObj` int(11) NOT NULL COMMENT '所在省份',
  `scenicTypeObj` int(11) NOT NULL COMMENT '景点类型',
  `dengji` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '景点等级',
  `scenicName` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '景点名称',
  `scenicPhoto` varchar(60) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '景点图片',
  `price` float NOT NULL COMMENT '门票价格',
  `openTime` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '开放时间',
  `address` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '景点地址',
  `scenicDesc` varchar(8000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '景点介绍',
  PRIMARY KEY (`scenicId`) USING BTREE,
  INDEX `provinceObj`(`provinceObj`) USING BTREE,
  INDEX `scenicTypeObj`(`scenicTypeObj`) USING BTREE,
  CONSTRAINT `t_scenic_ibfk_1` FOREIGN KEY (`provinceObj`) REFERENCES `t_province` (`provinceId`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `t_scenic_ibfk_2` FOREIGN KEY (`scenicTypeObj`) REFERENCES `t_scenictype` (`typeId`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_scenic
-- ----------------------------
INSERT INTO `t_scenic` VALUES (1, 1, 1, 'AAAA', '成都洛带古镇', 'img/7e5820b7-94d8-4cb9-baa1-3353e3e64973.jpg', 10, '全天开放', '成都龙泉镇北10公里', '<p>预定电话： 028-83929342</p>\r\n<p>&nbsp; &nbsp; 洛带古镇距离成都市中心约20公里，交通十分方便。\\r\\n公交车：可在成都市内乘71、81路、58路等车到达五桂桥汽车站，然后坐219路直接到洛带古镇。另外五桂桥汽车站有到龙泉的汽车，每几分钟就有一班。票价5元，下车后乘龙泉开往洛带的中巴车，票价3元。</p>\r\n<p>&nbsp; &nbsp;自驾车：洛带南距成渝高速公路龙泉站3.2公里，成洛、龙洪、龙新公路贯穿全境。从成都出发至洛带，仅需半个多小时，可当天往返。</p>');
INSERT INTO `t_scenic` VALUES (2, 1, 2, 'AAAAA', '宽窄巷子', 'img/2b513ffe-bdcd-4d3d-bdd7-451062af0ddc.jpg', 20, '早上8:30-晚上22:00', '成都市青羊区长顺上街127号', '<p>预定电话： 028-83920932</p>\r\n<p>宽窄巷子是到成都必需去的地方，过去老城都的感觉在这里都能体会到，要是有时间可以坐下来在露天的小院喝杯...</p>');

-- ----------------------------
-- Table structure for t_scenictype
-- ----------------------------
DROP TABLE IF EXISTS `t_scenictype`;
CREATE TABLE `t_scenictype`  (
  `typeId` int(11) NOT NULL AUTO_INCREMENT COMMENT '类型id',
  `typeName` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '类别名称',
  PRIMARY KEY (`typeId`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_scenictype
-- ----------------------------
INSERT INTO `t_scenictype` VALUES (1, '古镇');
INSERT INTO `t_scenictype` VALUES (2, '美食');

-- ----------------------------
-- Table structure for t_userinfo
-- ----------------------------
DROP TABLE IF EXISTS `t_userinfo`;
CREATE TABLE `t_userinfo`  (
  `user_name` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'user_name',
  `password` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '登录密码',
  `name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '姓名',
  `gender` varchar(4) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '性别',
  `birthDate` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '出生日期',
  `userPhoto` varchar(60) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户照片',
  `telephone` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '联系电话',
  `email` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '邮箱',
  `address` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '家庭地址',
  `regTime` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '注册时间',
  PRIMARY KEY (`user_name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_userinfo
-- ----------------------------
INSERT INTO `t_userinfo` VALUES ('user1', '123', '李晓明', '男', '2021-02-09', 'img/12.jpg', '13058010342', 'xiaoming@126.com', '四川成都红星路', '2021-02-17 11:34:34');
INSERT INTO `t_userinfo` VALUES ('user2', '123', '张晓霞', '女', '2021-02-04', 'img/8.jpg', '13508302934', 'xiaoxia@163.com', '四川成都崔家店路', '2021-02-17 11:47:27');

SET FOREIGN_KEY_CHECKS = 1;
