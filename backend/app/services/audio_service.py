import os
from flask import Response, request

CHUNK_SIZE = 1024 * 1024 # 1MB

def stream_audio(file_path):
    file_size = os.path.getsize(file_path)
    range_header = request.headers.get("Range", None)

    if not range_header:
        return Response(
            open(file_path, "rb"),
            mimetype= "audio/mpeg",
            headers={
                "Content-Length": str(file_size),
                "Accept-Ranges": "bytes",
            },
        )
    

    # Example: Range: byte=0-1023
    byte_range = range_header.replace("bytes=", "").split("-")
    start = int(byte_range[0])
    end = int(byte_range[1]) if byte_range[1] else start + CHUNK_SIZE
    end = min(end, file_size - 1)


    length = end - start + 1


    with open(file_path, "rb") as audio:
        audio.seek(start)
        data = audio.read(length)


    response = Response(
        data,
        206,
        mimetype="audio/mpeg",
        content_type="audio/mpeg",
        direct_passthrough=True,

    )

    response.headers.add("Content_Range", f"bytes {start}-{end}/{file_size}")
    response.headers.add("Accept-Ranges", "bytes")
    response.headers.add("Content-Length", str(length))


    return response