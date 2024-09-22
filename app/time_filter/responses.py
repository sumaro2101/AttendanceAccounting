from abc import ABC, abstractmethod
from typing import (Any,
                    ClassVar,
                    Dict,
                    List,
                    Optional,
                    Tuple,
                    Type,
                    )
import io
import csv
import tablib
from loguru import logger
import pandas as pd

from fastapi.responses import JSONResponse, Response, PlainTextResponse


class Renderer(ABC):
    media_types: ClassVar[Tuple[str, ...]] = None

    @abstractmethod
    def render(self,
               value: Any,
               status_code: int = 200,
               headers: Optional[Dict[str, str]] = None,
               media_type: Optional[str] = None):
        pass


class JSONRender(Renderer):
    media_types = ('application/json',)
    
    def render(self,
               value: Any,
               status_code: int = 200,
               headers: Optional[Dict[str, str]] = None,
               media_type: Optional[str] = None):
        return JSONResponse(value,
                            status_code=status_code,
                            headers=headers,
                            media_type=media_type,
                            )


class CSVRender(Renderer):
    media_types = ('file/csv',)

    def render(self,
               value: Any,
               status_code: int = 200,
               headers: Optional[Dict[str, str]] = None,
               media_type: Optional[str] = None):
        field_names = value[0].keys()
        logger.info(f'{self.__class__.__name__} get fields {field_names}')
        csv_in_memory = io.StringIO(newline='')
        writer = csv.DictWriter(
            csv_in_memory,
            fieldnames=field_names,
            quoting=csv.QUOTE_ALL
        )
        writer.writeheader()
        for data in value:
            writer.writerow(data)
        result = csv_in_memory.getvalue()
        logger.info(result)
        return Response(result,
                        headers=headers,
                        media_type=self.media_types[0])


class ExcelRender(Renderer):
    media_types = ('file/excel',)
    
    def render(self,
               value: Any,
               status_code: int = 200,
               headers: Optional[Dict[str, str]] = None,
               media_type: Optional[str] = None):
        headers_ex = list(value[0].keys())
        excel = tablib.Dataset(headers=headers_ex)
        for data in value:
            excel.append(row=data.values())
        result = pd.read_excel(excel.export('xlsx')).to_xml()
        logger.info(result)
        return PlainTextResponse(content=result,
                        status_code=status_code,
                        headers=headers,
                        media_type='application/xml',
                        )


@logger.catch(reraise=True)
def render(
    value: Any,
    accept: Optional[str],
    status_code: Optional[int],
    headers: Optional[Dict[str, str]],
    renderers: Optional[List[Type]] = None,
):
    """Render response taking into accout the requested media type in 'accept'"""
    renderers = renderers or [JSONRender, CSVRender, ExcelRender]
    if accept:
        for media_type in accept.split(','):
            media_type = media_type.split(';')[0].strip()
            for renderer in renderers:
                if media_type in renderer.media_types:
                    return renderer().render(value,
                                             status_code=status_code,
                                             headers=headers,
                                             media_type=media_type,
                                             )
    renderer = renderers[0]
    media_type = renderer.media_types[0]
    return renderer.render(value,
                           status_code=status_code,
                           headers=headers,
                           media_type=media_type,
                           )
