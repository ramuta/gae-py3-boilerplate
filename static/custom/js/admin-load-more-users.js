function adminLoadMoreUsers(cursor) {
    let months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

    let usersTable = document.getElementById("users-table");
    let usersButton = document.getElementById("loadMoreUsersButton");

    fetch('/admin/users?cursor='+cursor)
        .then(function(response) {
            return response.text();
        })
        .then(function(text) {
            data = JSON.parse(text);

            for (let user of data.users) {
                // a new row for the user object
                let userRow = document.createElement("tr");

                // set the name cell
                let userName = document.createElement("td");
                userName.innerHTML = "<a href='/admin/user/"+user.get_id+"'>"+user.first_name+" "+user.last_name+"</a>";
                userRow.appendChild(userName);

                // set the email cell
                let userEmail = document.createElement("td");
                userEmail.innerHTML = user.email_address;
                userRow.appendChild(userEmail);

                // set the date created cell
                let userCreated = document.createElement("td");
                let createdDate = new Date(user.created);
                userCreated.innerHTML = createdDate.getDate() + " " + months[createdDate.getMonth()] + " " + createdDate.getFullYear();
                userRow.appendChild(userCreated);

                // set the status cell
                let userStatus = document.createElement("td");

                if(user.admin) {
                    userStatus.innerHTML = '<span class="badge badge-warning">Admin</span>';
                } else {
                    userStatus.innerHTML = '<span class="badge badge-info">User</span>';
                }

                userRow.appendChild(userStatus);

                // append the user row to the users table
                usersTable.appendChild(userRow);
            }

            if(!data.more) {
                // if there's no more data to be loaded, hide the Load More button
                usersButton.style.display = "none";
            } else {
                // if there's more data to be loaded, set the next cursor in the onClick attribute on the button
                usersButton.setAttribute("onClick", "adminLoadMoreUsers('"+data.next_cursor+"')");
            }
        })
        .catch(function(error) {
            console.log('Request failed', error);
        });
}
