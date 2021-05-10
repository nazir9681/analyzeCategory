$(document).ready(function(){
    var catid = $( "#catid" ).val();
    var subid = $( "#subid" ).val();
      function loadData(page){
      $.ajax({
        url  : "/productPagination",
        type : "POST",
        cache: false,
        data : {page_no:page, catid:catid, subid:subid},
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

  function seeImages(id){
      $.ajax({
        url  : "/productImages",
        type : "POST",
        cache: false,
        data : {id: id},
        success:function(response){
          $("#productImage").html(response);
          $("#exampleModal").modal('show');
        }
    });
    
    }

    function deleteProduct(id){
      $.ajax({
        url  : "/removeproducts",
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