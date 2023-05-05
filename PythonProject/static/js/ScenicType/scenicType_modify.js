$(function () {
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/ScenicType/update/" + $("#scenicType_typeId_modify").val(),
		type : "get",
		data : {
			//typeId : $("#scenicType_typeId_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (scenicType, response, status) {
			$.messager.progress("close");
			if (scenicType) { 
				$("#scenicType_typeId_modify").val(scenicType.typeId);
				$("#scenicType_typeId_modify").validatebox({
					required : true,
					missingMessage : "请输入类型id",
					editable: false
				});
				$("#scenicType_typeName_modify").val(scenicType.typeName);
				$("#scenicType_typeName_modify").validatebox({
					required : true,
					missingMessage : "请输入类别名称",
				});
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#scenicTypeModifyButton").click(function(){ 
		if ($("#scenicTypeModifyForm").form("validate")) {
			$("#scenicTypeModifyForm").form({
			    url:"ScenicType/update/" + $("#scenicType_typeId_modify").val(),
			    onSubmit: function(){
					if($("#scenicTypeEditForm").form("validate"))  {
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
                	var obj = jQuery.parseJSON(data);
                    if(obj.success){
                        $.messager.alert("消息","信息修改成功！");
                        $(".messager-window").css("z-index",10000);
                        //location.href="frontlist";
                    }else{
                        $.messager.alert("消息",obj.message);
                        $(".messager-window").css("z-index",10000);
                    } 
			    }
			});
			//提交表单
			$("#scenicTypeModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});
