from src.session_manager import new_thread_id

def test_new_thread_id():
    thread_id = new_thread_id("juridique")
    assert thread_id.startswith("juridique-")
    assert len(thread_id) > len("juridique-")
