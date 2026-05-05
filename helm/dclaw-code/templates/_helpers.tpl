{{- define "dclaw-code.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "dclaw-code.fullname" -}}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s" $name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "dclaw-code.labels" -}}
helm.sh/chart: {{ include "dclaw-code.name" . }}-{{ .Chart.Version }}
app.kubernetes.io/name: {{ include "dclaw-code.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "dclaw-code.selectorLabels" -}}
app.kubernetes.io/name: {{ include "dclaw-code.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
