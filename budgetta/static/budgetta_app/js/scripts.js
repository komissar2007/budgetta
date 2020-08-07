function showExpense(name, amount, category, transactionId)
{
    $(".modal-body #transactionName").val( name );
    $(".modal-body #transactionAmount").val( amount );
    $(".modal-body #categoryText").val( category );
    $('#editExpenseModal').modal('show');
    $(".modal-body #transactionId").val( transactionId );
};

function showIncome(name, amount, category, transactionId)
{
    $(".modal-body #transactionName").val( name );
    $(".modal-body #transactionAmount").val( amount );
    $(".modal-body #categoryText").val( category );
    $('#editIncomeModal').modal('show');
    $(".modal-body #transactionId").val( transactionId );
};
