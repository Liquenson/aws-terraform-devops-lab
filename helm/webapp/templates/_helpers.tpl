{{- define "webapp.fullname" -}}webapp{{- end }}
{{- define "webapp.labels" -}}
app.kubernetes.io/name: webapp
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
{{- define "webapp.selectorLabels" -}}
app.kubernetes.io/name: webapp
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
