$(function () {
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/Province/update/" + $("#province_provinceId_modify").val(),
		type : "get",
		data : {
			//provinceId : $("#province_provinceId_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (province, response, status) {
			$.messager.progress("close");
			if (province) { 
				$("#province_provinceId_modify").val(province.provinceId);
				$("#province_provinceId_modify").validatebox({
					required : true,
					missingMessage : "请输入省份id",
					editable: false
				});
				$("#province_provinceName_modify").val(province.provinceName);
				$("#province_provinceName_modify").validatebox({
					required : true,
					missingMessage : "请输入省份名称",
				});
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#provinceModifyButton").click(function(){ 
		if ($("#provinceModifyForm").form("validate")) {
			$("#provinceModifyForm").form({
			    url:"Province/update/" + $("#province_provinceId_modify").val(),
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
			$("#provinceModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});
