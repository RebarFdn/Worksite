from apps.SiteProject.project import ( create_project, read_project, delete_project, get_workers , get_worker, all_projects, get_account)

def test_all_projects():
    result = all_projects()
    assert isinstance(result, list) 
    print("All Projects:", result)

def test_get_account():
    
    result = get_account(project_id="KS03093") # type: ignore
    assert result is not None
    print("Account:", result)

#test_all_projects()
test_get_account()