from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import User
from dashboard.models import PerfilUsuario, Curso, MaterialDidactico
from forum.models import Foro, Comentario
from resources.models import Recursos

# --------------------------
# Admin para usuarios con perfil
# --------------------------
class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil de Usuario'
    readonly_fields = ('foto_preview',)

    def foto_preview(self, obj):
        if obj.foto_perfil:
            return format_html('<img src="{}" width="80" style="border-radius:50%;"/>', obj.foto_perfil.url)
        return "No hay foto"
    foto_preview.short_description = "Foto"

class UserAdmin(admin.ModelAdmin):
    inlines = (PerfilUsuarioInline,)
    list_display = ('username', 'email', 'is_staff', 'is_teacher', 'institucion', 'foto_preview')
    search_fields = ('username', 'email', 'dashboard_perfil__institucion')
    list_filter = ('is_staff', 'is_superuser', 'dashboard_perfil__is_teacher')

    def is_teacher(self, obj):
        return obj.dashboard_perfil.is_teacher if hasattr(obj, 'dashboard_perfil') else False
    is_teacher.boolean = True
    is_teacher.short_description = 'Profesor'

    def institucion(self, obj):
        return obj.dashboard_perfil.institucion if hasattr(obj, 'dashboard_perfil') else "-"
    institucion.short_description = "Institución"

    def foto_preview(self, obj):
        if hasattr(obj, 'dashboard_perfil') and obj.dashboard_perfil.foto_perfil:
            return format_html('<img src="{}" width="50" style="border-radius:50%;"/>', obj.dashboard_perfil.foto_perfil.url)
        return "-"
    foto_preview.short_description = "Foto"

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# --------------------------
# Admin de Cursos
# --------------------------
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'grupo', 'profesor', 'numero_alumnos', 'ver_alumnos')
    search_fields = ('nombre', 'grupo', 'profesor__username')
    list_filter = ('grupo', 'profesor')

    def numero_alumnos(self, obj):
        return obj.alumnos.count()
    numero_alumnos.short_description = "Alumnos inscritos"

    def ver_alumnos(self, obj):
        alumnos = obj.alumnos.all()
        if alumnos:
            return format_html('<br>'.join([u.username for u in alumnos]))
        return "-"
    ver_alumnos.short_description = "Alumnos"

admin.site.register(Curso, CursoAdmin)

# --------------------------
# Admin de Material Didáctico
# --------------------------
class MaterialDidacticoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'fecha_subida', 'archivo_link', 'archivo_preview')
    search_fields = ('titulo', 'descripcion', 'tipo')
    list_filter = ('tipo', 'fecha_subida')

    def archivo_link(self, obj):
        if obj.archivo:
            return format_html('<a href="{}" target="_blank">Ver archivo</a>', obj.archivo.url)
        return "-"
    archivo_link.short_description = "Archivo"

    def archivo_preview(self, obj):
        if obj.archivo and obj.tipo in ["imagen", "image", "jpg", "png", "jpeg"]:
            return format_html('<img src="{}" width="80"/>', obj.archivo.url)
        return "-"
    archivo_preview.short_description = "Preview"

admin.site.register(MaterialDidactico, MaterialDidacticoAdmin)

# --------------------------
# Admin de Foros y Comentarios
# --------------------------
class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 0
    readonly_fields = ('autor', 'fecha')
    fields = ('autor', 'fecha', 'texto')
    show_change_link = True

class ForoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'fecha_creacion', 'fijado', 'link_foro')
    search_fields = ('titulo', 'descripcion', 'autor__username')
    list_filter = ('fijado', 'fecha_creacion')
    inlines = [ComentarioInline]
    actions = ['marcar_fijado', 'desmarcar_fijado']

    def link_foro(self, obj):
        return format_html('<a href="/admin/forum/foro/{}/change/">Abrir</a>', obj.id)
    link_foro.short_description = "Editar"

    def marcar_fijado(self, request, queryset):
        queryset.update(fijado=True)
    marcar_fijado.short_description = "Marcar como fijado"

    def desmarcar_fijado(self, request, queryset):
        queryset.update(fijado=False)
    desmarcar_fijado.short_description = "Desmarcar fijado"

admin.site.register(Foro, ForoAdmin)

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('foro', 'autor', 'fecha', 'texto_resumen')
    search_fields = ('foro__titulo', 'autor__username', 'texto')
    list_filter = ('fecha', 'autor')

    def texto_resumen(self, obj):
        return obj.texto[:50] + ("..." if len(obj.texto) > 50 else "")
    texto_resumen.short_description = "Comentario"

admin.site.register(Comentario, ComentarioAdmin)

# --------------------------
# Admin de Recursos
# --------------------------
class RecursosAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'completado', 'archivo_link', 'archivo_preview')
    search_fields = ('titulo', 'descripcion', 'autor__username')
    list_filter = ('completado',)  # eliminamos fecha_subida si no existe
    actions = ['marcar_completado', 'marcar_no_completado']

    def archivo_link(self, obj):
        if obj.archivo:
            return format_html('<a href="{}" target="_blank">Ver archivo</a>', obj.archivo.url)
        return "-"
    archivo_link.short_description = "Archivo"

    def archivo_preview(self, obj):
        if obj.archivo and obj.archivo.url.lower().endswith(('.jpg','.png','.jpeg','.gif')):
            return format_html('<img src="{}" width="80"/>', obj.archivo.url)
        return "-"
    archivo_preview.short_description = "Preview"

    def marcar_completado(self, request, queryset):
        queryset.update(completado=True)
    marcar_completado.short_description = "Marcar recursos como completados"

    def marcar_no_completado(self, request, queryset):
        queryset.update(completado=False)
    marcar_no_completado.short_description = "Marcar recursos como no completados"

admin.site.register(Recursos, RecursosAdmin)
