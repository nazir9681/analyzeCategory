$(document).ready(function(){
      var id = $( "#categoryid" ).val();
      var categoryname = $( "#categoryname" ).val();
        function loadData(page){
        $.ajax({
          url  : "/subcategoryPagination",
          type : "POST",
          cache: false,
          data : {page_no:page, id:id, categoryname:categoryname},
          success:function(response){
            $("#tableList").html(response);
          }
        });
      }
      loadData(page='');
      
      // Pagination code
      $(document).on("click", ".pagination li a", function(e){
        e.preventDefault();
        var pageId = $(this).attr("id");
        loadData(pageId);
      });
      });

      $("#submit").click(function(){
        $.ajax({
    
                type:'POST',
                url:'/insertSubcategory',
                data:$('#saveSubCategory').serialize(),
                success: function(data){ 
                  if(data.status == "true"){
                    location.reload();
                  }    
                  else{
                    alert("something went wrong");
                  }
                  
                }
            });
        });

        function deleteSubcategory(id){
          $.ajax({
            url  : "/removesubCategory",
            type : "POST",
            cache: false,
            data : {id: id},
            success:function(data){
              if(data.status == "true"){
                location.reload();
              }    
              else{
                alert("something went wrong");
              }
            }
        });
        
        }
        