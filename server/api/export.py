import pandas as pd
from fastapi.responses import StreamingResponse

def export_report(format: str):
    df = pd.read_sql("SELECT * FROM miners", db.engine)
    if format == "csv":
        return StreamingResponse(df.to_csv(index=False), media_type="text/csv")
    if format == "json":
        return df.to_json(orient="records")
    if format == "xlsx":
        out = io.BytesIO()
        df.to_excel(out, index=False)
        out.seek(0)
        return StreamingResponse(out, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")