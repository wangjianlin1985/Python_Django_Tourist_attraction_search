var province_manage_tool = null; 
$(function () { 
	initProvinceManageTool(); //建立Province管理对象
	province_manage_tool.init(); //如果需要通过下拉框查询，首先初始化下拉框的值
	$("#province_manage").datagrid({
		url : '/Province/list',
		queryParams: {
			"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
		},
		fit : true,
		fitColumns : true,
		striped : true,
		rownumbers : true,
		border : false,
		pagination : true,
		pageSize : 5,
		pageList : [5, 10, 15, 20, 25],
		pageNumber : 1,
		sortName : "provinceId",
		sortOrder : "desc",
		toolbar : "#province_manage_tool",
		columns : [[
			{
				field : "provinceId",
				title : "省份id",
				width : 70,
			},
			{
				field : "provinceName",
				title : "省份名称",
				width : 140,
			},
		]],
	});

	$("#provinceEditDiv").dialog({
		title : "修改管理",
		top: "50px",
		width : 700,
		height : 515,
		modal : true,
		closed : true,
		iconCls : "icon-edit-new",
		buttons : [{
			text : "提交",
			iconCls : "icon-edit-new",
			handler : function () {
				if ($("#provinceEditForm").form("validate")) {
					//验证表单 
					if(!$("#provinceEditForm").form("validate")) {
						$.messager.alert("错误提示","你输入的信息还有错误！","warning");
					} else {
						$("#provinceEditForm").form({
						    url:"/Province/update/" + $("#province_provinceId_edit").val(),
						    onSubmit: function(){
								if($("#provinceEditForm").form("validate"))  {
				                	$.messager.progress({
										text : "正在提交数据中...",
									});
				                	return true;
				                } else { 
				                    return false; 
				                }
						    },
						    success:function(data){
						    	$.messager.progress("close");
						    	console.log(data);
			                	var obj = jQuery.parseJSON(data);
			                    if(obj.success){
			                        $.messager.alert("消息","信息修改成功！");
			                        $("#provinceEditDiv").dialog("close");
			                        province_manage_tool.reload();
			                    }else{
			                        $.messager.alert("消息",obj.message);
			                    } 
						    }
						});
						//提交表单
						$("#provinceEditForm").submit();
					}
				}
			},
		},{
			text : "取消",
			iconCls : "icon-redo",
			handler : function () {
				$("#provinceEditDiv").dialog("close");
				$("#provinceEditForm").form("reset"); 
			},
		}],
	});
});

function initProvinceManageTool() {
	province_manage_tool = {
		init: function() {
		},
		reload : function () {
			$("#province_manage").datagrid("reload");
		},
		redo : function () {
			$("#province_manage").datagrid("unselectAll");
		},
		search: function() {
			$("#province_manage").datagrid("options").queryParams=queryParams; 
			$("#province_manage").datagrid("load");
		},
		exportExcel: function() {
			$("#provinceQueryForm").form({
			    url:"/Province/OutToExcel?csrfmiddlewaretoken" + $('input[name="csrfmiddlewaretoken"]').val(),
			});
			//提交表单
			$("#provinceQueryForm").submit();
		},
		remove : function () {
			var rows = $("#province_manage").datagrid("getSelections");
			if (rows.length > 0) {
				$.messager.confirm("确定操作", "您正在要删除所选的记录吗？", function (flag) {
					if (flag) {
						var provinceIds = [];
						for (var i = 0; i < rows.length; i ++) {
							provinceIds.push(rows[i].provinceId);
						}
						$.ajax({
							type : "POST",
							url : "/Province/deletes",
							data : {
								provinceIds : provinceIds.join(","),
								"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
							},
							beforeSend : function () {
								$("#province_manage").datagrid("loading");
							},
							success : function (data) {
								if (data.success) {
									$("#province_manage").datagrid("loaded");
									$("#province_manage").datagrid("load");
									$("#province_manage").datagrid("unselectAll");
									$.messager.show({
										title : "提示",
										msg : data.message
									});
								} else {
									$("#province_manage").datagrid("loaded");
									$("#province_manage").datagrid("load");
									$("#province_manage").datagrid("unselectAll");
									$.messager.alert("消息",data.message);
								}
							},
						});
					}
				});
			} else {
				$.messager.alert("提示", "请选择要删除的记录！", "info");
			}
		},
		edit : function () {
			var rows = $("#province_manage").datagrid("getSelections");
			if (rows.length > 1) {
				$.messager.alert("警告操作！", "编辑记录只能选定一条数据！", "warning");
			} else if (rows.length == 1) {
				$.ajax({
					url : "/Province/update/" + rows[0].provinceId,
					type : "get",
					data : {
						//provinceId : rows[0].provinceId,
					},
					beforeSend : function () {
						$.messager.progress({
							text : "正在获取中...",
						});
					},
					success : function (province, response, status) {
						$.messager.progress("close");
						if (province) { 
							$("#provinceEditDiv").dialog("open");
							$("#province_provinceId_edit").val(province.provinceId);
							$("#province_provinceId_edit").validatebox({
								required : true,
								missingMessage : "请输入省份id",
								editable: false
							});
							$("#province_provinceName_edit").val(province.provinceName);
							$("#province_provinceName_edit").validatebox({
								required : true,
								missingMessage : "请输入省份名称",
							});
						} else {
							$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
						}
					}
				});
			} else if (rows.length == 0) {
				$.messager.alert("警告操作！", "编辑记录至少选定一条数据！", "warning");
			}
		},
	};
}
