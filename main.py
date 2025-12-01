if __name__ == "__main__":
    pass

else:
    from app.infra.api import create_app

    app = create_app()

__all__ = ("app",)
