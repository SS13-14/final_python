from flask import jsonify, request
from sqlalchemy import func
from app import app, connection, text, render_template


@app.route('/admin/user')
def indexUser():
    return render_template(
        'admin/user/index.html',
        module='user',
    )


@app.route('/api/user')
def getAllUsers():  # Update the method name here
    result = connection.execute(text("SELECT * FROM user"))
    user_arr = []
    for item in result:
        user_arr.append({
            'id': item.id,
            'name': item.name,
            'image': item.image,
            'status': item.status,
        })
    return jsonify(user_arr)


@app.route('/api/user', methods=['POST'])
def addUser():
    try:
        data = request.json
        # Extract user data from JSON
        name = data.get('name')
        image = data.get('image')
        status = data.get('status')

        # Insert the new user into the database
        result = connection.execute(text("INSERT INTO user (name, image, status) VALUES (:name, :image, :status)"), {
            'name': name,
            'image': image,
            'status': status,
        })

        # Get the last inserted user ID using the LAST_INSERT_ID() function
        user_id = connection.execute(text("SELECT LAST_INSERT_ID()")).fetchone()[0]

        # Fetch the inserted user from the database
        result = connection.execute(text("SELECT * FROM user WHERE id = :user_id"), {'user_id': user_id})
        user = result.fetchone()

        return jsonify(
            {'success': True, 'user': {'id': user.id, 'name': user.name, 'image': user.image, 'status': user.status}})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/user/<int:id>', methods=['DELETE'])
def deleteUser(id):
    try:
        # Delete the user from the database based on the provided ID
        connection.execute(text("DELETE FROM user WHERE id = :id"), {'id': id})
        return jsonify({'success': True, 'message': 'User has been deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/user/<int:id>', methods=['PUT'])
def editUser(id):
    try:
        data = request.json
        # Update the user in the database based on the provided ID
        connection.execute(text("UPDATE user SET name = :name, image = :image, status = :status WHERE id = :id"), {
            'name': data.get('name'),
            'image': data.get('image'),
            'status': data.get('status'),
            'id': id,
        })
        return jsonify({'success': True, 'message': 'User has been updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
