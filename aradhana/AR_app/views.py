from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SalesRecord, Inventory, Data
from .serializers import SalesRecordSerializer, InventorySerializer, DataSerializer
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler  # Import StandardScaler
from django.http import HttpResponse
import os

class PredictionAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Load the saved model
            model_path = os.path.join('Model', 'profit_prediction_model.pkl')  # Ensure the path is correct
            if not os.path.exists(model_path):
                return Response({"error": "Model file not found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            with open(model_path, 'rb') as model_file:
                model = pickle.load(model_file)

            # Fetch all records from the 'data' table
            data_records = Data.objects.all()
            serializer = DataSerializer(data_records, many=True)
            data = serializer.data

            # Prepare to collect unique seasons and calculate total profit
            season_data = {}
            for record in data:
                season = record['season']
                profit = record.get('profit', 0.0)

                # Initialize the season in the dictionary if not already present
                if season not in season_data:
                    season_data[season] = {
                        'total_profit': 0.0,
                        'count': 0
                    }

                # Accumulate the profit for each season
                season_data[season]['total_profit'] += float(profit)
                season_data[season]['count'] += 1

            # Ensure there are enough unique seasons to choose from
            unique_seasons = list(season_data.keys())
            if len(unique_seasons) < 2:
                return Response({"error": "Not enough unique seasons available for prediction."}, status=status.HTTP_400_BAD_REQUEST)

            # Take only the first two unique seasons
            selected_seasons = unique_seasons[:2]

            # Prepare response data
            response_data = []
            for season in selected_seasons:
                total_profit = season_data[season]['total_profit']  # Total profit for this season

                # Use the same encoding/scaling as during training
                # Assuming that we scale profit data
                scaler = StandardScaler()
                total_profit_scaled = scaler.fit_transform([[total_profit]])

                season_encoded = hash(season) % 1000  # Simplified encoding example

                # Prepare input array for the model
                # Replace this placeholder with the actual third feature's value
                third_feature = 0.0  # Placeholder; this should be replaced with the actual value if available

                X = np.array([[total_profit_scaled[0][0], season_encoded, third_feature]])  # 3 features as expected by the model

                # Make a prediction using the loaded model
                predicted_profit = model.predict(X)[0]

                # Prepare the response data
                response_data.append({
                    "profit": total_profit,  # Total profit for the season
                    "season": season,
                    "predicted_profit": predicted_profit
                })

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# SalesRecord ViewSet
class SalesRecordViewSet(viewsets.ModelViewSet):
    queryset = SalesRecord.objects.all()
    serializer_class = SalesRecordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Inventory ViewSet
class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Data ViewSet
class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
