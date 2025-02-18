
# Include necessary Capella Modeller API
include('workspace://Python4Capella/simplified_api/capella.py')
if False:
    from simplified_api.capella import *

# Include requirement API
include('workspace://Python4Capella/simplified_api/requirement.py')
if False:
    from simplified_api.requirement import *

# Include utilities
include('workspace://Python4Capella/utilities/CapellaPlatform.py')
if False:
    from utilities.CapellaPlatform import *
    
# ------------------------------------------------------------------
# Standard imports and Java integration
# ------------------------------------------------------------------
import eclipse.system.ui as ui  # @UnresolvedImport
from py4j.java_gateway import java_import

# Access the JVM via the py4j gateway
jvm = gateway.jvm  # @UndefinedVariable
java_import(jvm, 'org.polarsys.capella.core.model.handler.helpers.CapellaAdapterHelper')
CapellaAdapterHelper = jvm.org.polarsys.capella.core.model.handler.helpers.CapellaAdapterHelper

# ------------------------------------------------------------------
# Scenario Definition: Entities and Relationships
# ------------------------------------------------------------------
entities = [
    {"name": "Customer", "description": "A customer who places orders."},
    {"name": "Product", "description": "A product available for purchase."},
    {"name": "Order", "description": "An order placed by a customer."},
    {"name": "Payment", "description": "A payment made for an order."}
]

relations = [
    {"source": "Customer", "target": "Order", "type": "places"},
    {"source": "Order", "target": "Product", "type": "contains"},
    {"source": "Order", "target": "Payment", "type": "associated with"}
]

# ------------------------------------------------------------------
# Function to update the diagram with entities and relationships
# ------------------------------------------------------------------
def update_diagram(entities, relations):
    """
    Retrieves the selected Operational Entity Breakdown diagram,
    updates the model with new entities and relationships.
    """
    # Retrieve active selection from Eclipse
    selected = ui.getSelection()
    selected_list = selected.toList()
    if not selected_list or len(selected_list) == 0:
        print("No active selection. Please select a diagram.")
        return

    # Resolve semantic elements from the selection
    semantic_elements = CapellaAdapterHelper.resolveSemanticObjects(selected_list, True)
    if not semantic_elements or len(semantic_elements) == 0:
        print("No semantic element resolved from selection. Please select a valid diagram.")
        return

    # Assume first resolved semantic element is the diagram representation
    diagram_representation = semantic_elements[0]

    # Retrieve the **semantic model root element** from the diagram
    semantic_root = diagram_representation.eContainer()  # Get the semantic container

    if not semantic_root:
        print("Could not retrieve the semantic model from the diagram.")
        return

    # Print the type of the semantic model to verify
    print(f"Semantic model type: {type(semantic_root)}")

    # Retrieve model path
    session = Sirius.get_session(diagram_representation)
    res = session.getSessionResource().getURI().toPlatformString(True)
    model_path = "/" + res[1:res.rfind(".")] + ".aird"
    print("Model path:", model_path)

    # Open the Capella model
    model = CapellaModel()
    model.open(model_path)

    # Start a transaction to update the model
    model.start_transaction()
    try:
        # Dictionary to track created entities
        entity_objs = {}

        # Create or update entities
        for ent in entities:
            name = ent.get("name")
            desc = ent.get("description")
            if not name:
                continue

            # Check if entity exists in the **semantic model**
            existing_entity = None
            for obj in semantic_root.getOwnedElements():  # Generic check for owned elements
                if obj.getName() == name:
                    existing_entity = obj
                    break

            if existing_entity is None:
                print(f"Creating entity: {name}")

                # Dynamically find the correct method
                if hasattr(semantic_root, "createEntity"):
                    new_entity = semantic_root.createEntity(name)
                elif hasattr(semantic_root, "createComponent"):
                    new_entity = semantic_root.createComponent(name)
                elif hasattr(semantic_root, "createOwnedOperationalEntity"):
                    new_entity = semantic_root.createOwnedOperationalEntity(name)
                else:
                    print(f"ERROR: No valid method found to create an entity for {name}")
                    continue
            else:
                print(f"Updating entity: {name}")
                new_entity = existing_entity

            new_entity.setDescription(desc)
            entity_objs[name] = new_entity

        # Create relationships
        for rel in relations:
            source_name = rel.get("source")
            target_name = rel.get("target")
            relation_type = rel.get("type")

            source_obj = entity_objs.get(source_name)
            target_obj = entity_objs.get(target_name)

            if not source_obj or not target_obj:
                print(f"Missing entity in relation: {source_name} {relation_type} {target_name}")
                continue

            # Check if relationship already exists
            existing_rel = False
            if hasattr(source_obj, "getOwnedRelationships"):
                for existing_relation in source_obj.getOwnedRelationships():
                    if existing_relation.getTarget() == target_obj:
                        existing_rel = True
                        break

            if not existing_rel:
                print(f"Creating relation: {source_name} {relation_type} {target_name}")
                if hasattr(source_obj, "createOwnedRelationship"):
                    new_relation = source_obj.createOwnedRelationship(target_obj)
                    new_relation.setName(relation_type)
                else:
                    print(f"ERROR: No valid method found to create relationship {relation_type}")

        # Commit changes
        model.commit_transaction()
        print("Diagram updated successfully.")
    except Exception as e:
        model.rollback_transaction()
        print("Error during diagram update:", e)
    finally:
        # Save model changes
        model.save()
        print("Model saved successfully.")

# ------------------------------------------------------------------
# Main execution: Update diagram based on scenario
# ------------------------------------------------------------------
if __name__ == '__main__':
    update_diagram(entities, relations)
