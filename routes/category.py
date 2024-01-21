from flask import jsonify, request

from app import app, connection, text, render_template


@app.route('/admin/category')
def indexCategory():
    return render_template(
        'admin/category/index.html',
        module='category',
    )


@app.route('/api/category')
def getAllCategory():
    result = connection.execute(text("SELECT * FROM category"))
    category_arr = []
    for item in result:
        category_arr.append({
            'id': item.id,
            'name': item.name,
        })
    return jsonify(category_arr)


@app.route('/api/category', methods=['POST'])
def addCategory():
    try:
        data = request.json  # Assuming the data is sent as JSON in the request body
        name = data.get('name')
        # Insert the new category into the database
        connection.execute(text("INSERT INTO category (name) VALUES (:name)"), {'name': name})
        return jsonify({'success': True, 'message': 'Category added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/category/<int:id>', methods=['DELETE'])
def deleteCategory(id):
    try:
        # Delete the category from the database based on the provided ID
        connection.execute(text("DELETE FROM category WHERE id = :id"), {'id': id})
        return jsonify({'success': True, 'message': 'Category deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/category/<int:id>', methods=['PUT'])
def editCategory(id):
    try:
        data = request.json  # Assuming the data is sent as JSON in the request body
        new_name = data.get('name')
        # Update the category in the database based on the provided ID
        connection.execute(text("UPDATE category SET name = :name WHERE id = :id"), {'name': new_name, 'id': id})
        return jsonify({'success': True, 'message': 'Category updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})