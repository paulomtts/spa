"""
Defines the BaseComponent for all server-side UI components.
This class holds a reference to the Jinja2 template engine.
"""

import inspect
from fastapi.templating import Jinja2Templates
from markupsafe import Markup
from pydantic import BaseModel


class BaseComponent(BaseModel):
    _engine: "Jinja2Templates" = None
    _path: str = ""

    def __init_subclass__(cls, **kwargs):
        """Ensures that any component inheriting from this base has a template path."""
        super().__init_subclass__(**kwargs)

        # Auto-derive template path from file location if not explicitly set
        if "_template" not in cls.__dict__ or not cls.__dict__["_template"]:
            file_path = inspect.getfile(cls)
            # Find the 'templates' directory in the path
            parts = file_path.replace("\\", "/").split("/")
            if "templates" in parts:
                idx = parts.index("templates")
                template_parts = parts[idx + 1 :]  # everything after 'templates/'
                # For component files, use directory name for the template
                if len(template_parts) >= 3 and template_parts[0] == "components":
                    component_dir = template_parts[1]
                    template_parts = [
                        "components",
                        component_dir,
                        f"{component_dir}.html",
                    ]
                cls._path = "/".join(template_parts)
            else:
                raise NotImplementedError(
                    f"Could not auto-derive template path for {cls.__name__}. "
                    "Please define a '_template' class variable or ensure the file is in the templates/ directory."
                )

    @property
    def html(self) -> Markup:
        """
        Property that automatically renders the component when accessed.
        This allows for cleaner template syntax: {{ component.html }} instead of {{ component.render() }}
        """
        return self._render()

    @classmethod
    def set_engine(cls, templates: "Jinja2Templates"):
        """
        Sets the Jinja2 templates engine for all components
        that inherit from this base class.
        This should be called once at application startup.
        """
        cls._engine = templates

    @classmethod
    def get_engine(cls) -> "Jinja2Templates":
        """
        Gets the configured Jinja2 templates engine.
        Raises an error if the engine has not been set.
        """
        if not cls._engine:
            raise ValueError(
                "Templates engine not set. "
                "Call BaseComponent.set_engine() at application startup."
            )
        return cls._engine

    def _render(self, **context) -> Markup:
        """
        Renders the component's template with the given context.
        The context is automatically supplemented with the component's own data.
        """
        engine = self.get_engine()
        template = engine.get_template(self.__class__._path)

        full_context = self.model_dump()
        full_context.update(context)

        return Markup(template.render(full_context))
