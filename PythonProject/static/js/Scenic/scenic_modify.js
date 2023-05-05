$(function () {
    //实例化景点介绍编辑器
    tinyMCE.init({
        selector: "#scenic_scenicDesc_modify",
        theme: 'advanced',
        language: "zh",
        strict_loading_mode: 1,
    });
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/Scenic/update/" + $("#scenic_scenicId_modify").val(),
		type : "get",
		data : {
			//scenicId : $("#scenic_scenicId_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (scenic, response, status) {
			$.messager.progress("close");
			if (scenic) { 
				$("#scenic_scenicId_modify").val(scenic.scenicId);
				$("#scenic_scenicId_modify").validatebox({
					required : true,
					missingMessage : "请输入景点id",
					editable: false
				});
				$("#scenic_provinceObj_provinceId_modify").combobox({
					url:"/Province/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"provinceId",
					textField:"provinceName",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#scenic_provinceObj_provinceId_modify").combobox("select", scenic.provinceObjPri);
						//var data = $("#scenic_provinceObj_provinceId_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#scenic_provinceObj_provinceId_edit").combobox("select", data[0].provinceId);
						//}
					}
				});
				$("#scenic_scenicTypeObj_typeId_modify").combobox({
					url:"/ScenicType/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"typeId",
					textField:"typeName",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#scenic_scenicTypeObj_typeId_modify").combobox("select", scenic.scenicTypeObjPri);
						//var data = $("#scenic_scenicTypeObj_typeId_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#scenic_scenicTypeObj_typeId_edit").combobox("select", data[0].typeId);
						//}
					}
				});
				$("#scenic_dengji_modify").val(scenic.dengji);
				$("#scenic_dengji_modify").validatebox({
					required : true,
					missingMessage : "请输入景点等级",
				});
				$("#scenic_scenicName_modify").val(scenic.scenicName);
				$("#scenic_scenicName_modify").validatebox({
					required : true,
					missingMessage : "请输入景点名称",
				});
				$("#scenic_scenicPhotoImgMod").attr("src", scenic.scenicPhoto);
				$("#scenic_price_modify").val(scenic.price);
				$("#scenic_price_modify").validatebox({
					required : true,
					validType : "number",
					missingMessage : "请输入门票价格",
					invalidMessage : "门票价格输入不对",
				});
				$("#scenic_openTime_modify").val(scenic.openTime);
				$("#scenic_openTime_modify").validatebox({
					required : true,
					missingMessage : "请输入开放时间",
				});
				$("#scenic_address_modify").val(scenic.address);
				$("#scenic_address_modify").validatebox({
					required : true,
					missingMessage : "请输入景点地址",
				});
				tinyMCE.editors['scenic_scenicDesc_modify'].setContent(scenic.scenicDesc);
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#scenicModifyButton").click(function(){ 
		if ($("#scenicModifyForm").form("validate")) {
			$("#scenicModifyForm").form({
			    url:"Scenic/update/" + $("#scenic_scenicId_modify").val(),
			    onSubmit: function(){
					if($("#scenicEditForm").form("validate"))  {
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
			$("#scenicModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});
