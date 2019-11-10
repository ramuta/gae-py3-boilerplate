function adminLoadMoreUsers(cursor) {
    console.log("admin load more users");
    console.log(cursor);

    let usersTable = document.getElementById("users-table");
    let usersButton = document.getElementById("loadMoreUsersButton");

    fetch('/admin/users?cursor='+cursor)
        .then(function(response) {
            return response.text();
        })
        .then(function(text) {
            data = JSON.parse(text);

            for (let user of data.users) {
                let userRow = document.createElement("tr");

                let userName = document.createElement("td");
                userName.innerHTML = "<a href='/admin/user/"+user.get_id+"'>"+user.first_name+" "+user.last_name+"</a>";
                userRow.appendChild(userName);

                let userEmail = document.createElement("td");
                userEmail.innerHTML = user.email_address;
                userRow.appendChild(userEmail);

                let userCreated = document.createElement("td");
                userCreated.innerHTML = user.created;
                userRow.appendChild(userCreated);

                let userStatus = document.createElement("td");

                if(user.admin) {
                    userStatus.innerHTML = '<span class="badge badge-warning">Admin</span>';
                } else {
                    userStatus.innerHTML = '<span class="badge badge-info">User</span>';
                }

                userRow.appendChild(userStatus);

                usersTable.appendChild(userRow);
            }

            if(!data.more) {
                usersButton.style.display = "none";
            } else {
                usersButton.setAttribute("onClick", "adminLoadMoreUsers('"+data.next_cursor+"')");
            }
        })
        .catch(function(error) {
            console.log('Request failed', error);
        });
}
