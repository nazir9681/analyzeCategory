$(document).ready(function(){
  function loadData(page){
    $.ajax({
      url  : "/categoryPagination",
      type : "POST",
      cache: false,
      data : {page_no:page},
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
            url:'/insertCategory',
            data:$('#saveCategory').serialize(),
            success: function(data){
              // var jsondata =JSON.parse(data)
              // var status=jsondata.status; 
              // alert(status)  
              if(data.status == "true"){
                location.reload();
              }    
              else{
                alert("something went wrong");
              }
              
            }
        });
    });

function deleteCategory(id){
      $.ajax({
        url  : "/removeCategory",
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

    