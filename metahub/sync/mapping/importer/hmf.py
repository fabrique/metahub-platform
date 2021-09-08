from datetime import datetime
from typing import List

from pydantic import BaseModel

from metahub.collection.models import BaseCollectionArtist
from metahub.sync.mapping.importer import Dating, Creator, TypeTextNotes, OtherObject, Publication, Image, Artist


class Object(BaseModel):
    Id: int
    # CreateUser: str
    # CreateDate: datetime
    ChangeUser: str
    ChangeDate: datetime
    ReferenceNumber: str = ""
    ShortTitle: str = ""
    ObjectName: str = ""
    Datings: List[Dating] = []
    Dating: str = ""
    ContainerName: str = ""
    ContainerId: int = 0
    Creditline: str = ""
    Credits: str = ""
    ShortText: str = ""
    ReadMore: str = ""
    AcquisitionDate: str = ""
    CurrentLocation: str = ""
    Convolute: str = ""
    NumberOfParts: str = ""
    Creators: List[Creator] = []
    Provenance: List[TypeTextNotes] = []
    GeoReference: List[TypeTextNotes] = []
    Dimensions: str = ""
    MaterialTechnique: str = ""
    Signatures: List[TypeTextNotes] = []
    # Inscriptions: List[TypeTextNotes]
    Keywords: List[TypeTextNotes] = []
    OtherObjects: List[OtherObject] = []
    Publications: List[Publication] = []
    IsHighlight: bool = False
    Exhibitions: List[TypeTextNotes] = []
    ImageLicense: str = ""
    Images: List[Image] = []
    Artists_Active: List[Artist] = []

    def to_bc_dict(self):
        return dict(
            bc_id=self.Id,
            bc_inventory_number=self.ReferenceNumber,
            bc_change_date=self.ChangeDate,
            bc_change_user=self.ChangeUser,
            bc_object_name=self.ObjectName,
            bc_credits=self.Creditline,
            bc_notes=f"{self.ShortText}\n{self.ReadMore}",
            bc_tags="|".join(self.get_tags()),
            bc_images=", ".join([i.KeyFileName for i in self.Images]),
            bc_image_license=self.Credits, #, ".join([i.License for i in self.Images]),
            date_acquired=self.AcquisitionDate,
            datings=self.Dating or "Unbekannt",
            dating_from_df=self.Datings[0].year_from_date() if self.Datings else None,
            dating_to_df=self.Datings[0].year_to_date() if self.Datings else None,
            provenance=", ".join(
                [f"{p.Notes}: {p.Text}" for p in self.Provenance if p.Text]
            ),
            signatures=", ".join(
                [f"{s.Text} {s.Type}" for s in self.Signatures if s.Text and s.Type]
            ),
            publications=", ".join(
                [
                    f"{p.Text.strip()}- {p.specifications()}"
                    for p in self.Publications
                    if p.Text
                ]
            ),
            is_highlight=self.IsHighlight,
            current_location=self.CurrentLocation,
            container_name=self.ContainerName,
            container_id=self.ContainerId,
            geographic_reference=", ".join([i.Text for i in self.GeoReference]),
            geographic_location=", ".join([i.Text for i in self.GeoReference]),
            convolute=self.Convolute,
            series_id=self.get_series_id(),
            material=self.MaterialTechnique,
            dimensions=self.Dimensions,
            title=self.ShortTitle,
            artist=self.get_artist_for_object(self.Artists_Active, self.Id),
            object_type=self.get_keyword_text("Objektbezeichnung"),
        )

    def get_artist_for_object(self, artist_data, object_id):
        """
        Artists have been added to the DB before objects are synced, so normally
        every object that mentions an artist can find the match.
        """
        artist_id = artist_data[0].ArtistId if artist_data else None

        try:
            artist = BaseCollectionArtist.objects.get(bc_inventory_number=artist_id)
            print('Found artist {} for object {}'.format(artist, object_id))
        except BaseCollectionArtist.DoesNotExist:
            print('Cannot find artist with id {} for object {}'.format(artist_id, object_id))
            artist = None
        return artist


    def get_tags(self):
        for tag in self.Keywords:
            if tag.Type == "Inhalt/Kontext" and "(" in tag.Text:
                yield tag.Text.split("(")[0].strip()

    def get_keyword_text(self, type):
        keywords = [k for k in self.Keywords if k.Type == type]
        if keywords and "(" in keywords[0]:
            return keywords[0].Text.split("(")[0].strip()
        return "Unbekannt"

    def get_series_id(self):
        if self.OtherObjects:
            parts = self.ReferenceNumber.split("-")
            if parts:
                if len(parts) >= 3:
                    return parts[0] + parts[1]

    def get_title(self):
        return self.ShortTitle
