function showSuccessModal() {
    const modalElement = document.getElementById('Success');
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
}

// 删除类型
function deleteType(type_id) {
    if (confirm('确定要进行此操作吗？')) {
        fetch(`/manager/deltype/${type_id}`, {
            method: 'DELETE',
        })
            .then(response => response.json())
            .then(data => {
                if (data.message === 'success') {
                    // 删除表格中的对应行
                    const row = document.getElementById(type_id);
                    const option = document.getElementById(`option-${type_id}`);
                    if (row && option) {
                        row.remove();
                        option.remove();
                        showSuccessModal();
                    }
                }
            })
            .catch(error => {
                alert('出错了！');
            });
    }
}

// 添加类型
function addType() {
    const typeName = document.getElementById('InputName').value;
    if (!typeName) {
        alert('类型名称不能为空！');
        return;
    }

    fetch('/manager/addtype', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({name: typeName}),
    })
        .then(response => response.json())
        .then(data => {
            if (data.message === 'success') {
                // 添加新行到表格
                const typeList = document.getElementById('type-list').getElementsByTagName('tbody')[0];
                const newRow = document.createElement('tr');
                newRow.id = `${data.id}`;
                newRow.innerHTML = `
                        <th scope="row">${data.id}</th>
                        <td>${data.name}</td>
                        <td>
                            <button type="button" class="btn btn-primary" onclick="deleteType(${data.id})">删除</button>
                        </td>
                    `;
                typeList.appendChild(newRow);

                // 添加新选项到添加图书的页面
                const selectElement = document.getElementById('BookType');
                const newOption = new Option(`${data.name}`, `${data.id}`);
                selectElement.appendChild(newOption);

                // 清空输入框
                document.getElementById('InputName').value = '';

                // 显示操作成功的 Toast
                showSuccessModal();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('出错了！');
        });
}

// 添加图书
function addBook() {
    const bookName = document.getElementById('BookName').value;
    const bookAuthor = document.getElementById('BookAuthor').value;
    const bookType = document.getElementById('BookType').value;
    if (!bookName || !bookAuthor || !bookType) {
        alert('各属性不能为空！');
        return;
    }

    fetch('/manager/addbook', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({name: bookName, author: bookAuthor, type: bookType}),
    })
        .then(response => response.json())
        .then(data => {
            if (data.message === 'success') {

                // 清空内容
                document.getElementById('BookName').value = '';
                document.getElementById('BookAuthor').value = '';
                document.getElementById('BookType').value = '';

                // 显示成功Modal
                showSuccessModal();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('出错了！');
        });
}

// 删除图书
function deleteBook(book_id) {
    if (confirm('确定要进行此操作吗？')) {
        fetch(`/manager/delbook/${book_id}`, {
            method: 'DELETE',
        })
            .then(response => response.json())
            .then(data => {
                if (data.message === 'success') {
                    // 删除表格中的对应行
                    const row = document.getElementById(`book-${book_id}`);
                    if (row) {
                        row.remove();
                        showSuccessModal();
                    }
                }
            })
            .catch(error => {
                alert('出错了！');
            });
    }
}

// 获取图书信息用于修改
function putBookInfo(book_id, book_name, book_author, book_type) {
    console.log("puting");
    // 监听模态框的显示事件
    const editBookModal = document.getElementById('EditBook');
    editBookModal.addEventListener('shown.bs.modal', function () {
        // 设置 placeholder 和选中项
        document.getElementById('EditBookId').value = book_id;
        document.getElementById('EditBookName').value = book_name;
        document.getElementById('EditBookAuthor').value = book_author;

        const bookTypeSelector = document.getElementById('EditBookType');
        if (bookTypeSelector) {
            for (let option of bookTypeSelector.options) {
                if (option.value == book_type) {
                    option.selected = true;
                    break;
                }
            }
        }
        console.log("bookinfo put.");
    });
}

// 修改图书
function EditBook() {
    const bookId = document.getElementById('EditBookId').value;
    const bookName = document.getElementById('EditBookName').value;
    const bookAuthor = document.getElementById('EditBookAuthor').value;
    const bookType = document.getElementById('EditBookType').value;
    if (!bookName || !bookAuthor || !bookType) {
        alert('各属性不能为空！');
        return;
    }

    fetch('/manager/editbook', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({id: bookId, name: bookName, author: bookAuthor, type: bookType}),
    })
        .then(response => response.json())
        .then(data => {
            if (data.message === 'success') {
                // 显示成功Modal
                showSuccessModal();
            } else if (data.message === 'error') {
                console.log('error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('出错了！');
        });
}

// 借阅
function BorrowBook(book_id) {
    fetch(`/user/borrow/${book_id}`, {
        method: 'POST',
    })
        .then(response => response.json())
        .then(data => {
            if (data.message === 'success') {
                // 删除表格中的对应行
                const row = document.getElementById(`book-${book_id}`);
                if (row) {
                    row.remove();
                    showSuccessModal();
                }
            }
        })
        .catch(error => {
            alert('出错了！');
        });
}

// 用户归还
function ReturnBook(borrow_id) {
    fetch(`/user/return/${borrow_id}`, {
        method: 'POST',
    })
        .then(response => response.json())
        .then(data => {
            if (data.message === 'success') {
                // 删除表格中的对应行
                const row = document.getElementById(`borrow-${borrow_id}`);
                if (row) {
                    row.remove();
                    showSuccessModal();
                }
            }
        })
        .catch(error => {
            alert('出错了！');
        });
}