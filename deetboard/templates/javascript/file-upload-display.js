<script>

	$("form input[class='file-upload']").change(function () { 
	    
	    var fullPath = $(this).val();
	    
	    var filename = fullPath.replace(/^.*[\\\/]/, '');

	    $("#upload-file-info").html(filename);
	    
	});
	
</script>