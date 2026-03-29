from apps.SiteProject.project import ( create_project, read_project, delete_project, get_workers , get_worker, all_projects)

def test_all_projects():
    result = all_projects()
    assert isinstance(result, list) 
    print("All Projects:", result)

def test_create_project():
    data = {
        "name": "Test Project",
        "description": "This is a test project.",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31"
    }
    result = create_project(data=data)
    assert result is not None
    assert hasattr(result, 'inserted_id')

test_all_projects()