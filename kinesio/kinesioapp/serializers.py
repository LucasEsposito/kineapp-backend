from rest_framework import serializers
from .models import Medic, ClinicalHistory, ClinicalSession, Patient, SecretQuestion, SecretAnswer
from users.serializers import PatientSerializer

class PatientSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(format="%Y-%m-%d")
    finish_date = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Patient
        fields = ('username', 'name', 'last_name', 'start_date', 'finish_date')


class MedicSerializer(serializers.ModelSerializer):
    patients = PatientSerializer(many=True, required=False)

    class Meta:
        model = Medic
        fields = ('username', 'name', 'last_name', 'license', 'patients')


class ClinicalSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClinicalSession
        fields = ('date', 'status', 'clinical_history')


class ClinicalHistorySerializer(serializers.ModelSerializer):
    clinical_sessions = ClinicalSessionSerializer(many=True, required=False)
    patient_id = serializers.IntegerField(write_only=True)
    patient = PatientSerializer(read_only=True)

    class Meta:
        model = ClinicalHistory 
        fields = ('date', 'description', 'status', 'patient_id', 'patient', 'clinical_sessions')

class SecretQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SecretQuestion
        fields = ('__all__')

class SecretAnswerSerializer(serializers.ModelSerializer):
    medic = MedicSerializer(read_only=True)
    medic_id = serializers.IntegerField(write_only=True)
    question = SecretQuestionSerializer(read_only=True)
    question_id = serializers.IntegerField(write_only=True)
    answer = serializers.CharField(write_only=True)
    #depth = 1

    class Meta:
        model = SecretAnswer
        fields = ('medic', 'question', 'answer', 'question_id', 'medic_id')

