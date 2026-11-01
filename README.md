##### ECR

###### 1\. overview

The Executable Cell Runtime (ECR) is a computational framework prototype designed to model the dynamic interactions between cells and their microenvironments. It aims to explicitly represent how cells perceive external environmental conditions, process intracellular information, generate decisions, and subsequently modify their internal states and surrounding environments through a layered architecture. ECR integrates environmental representation with intracellular information processing by placing cells and their surrounding signaling fields (Fields) within a two-dimensional spatial grid (World 2D). This representation captures the spatial distribution of cells and their interactions with the extracellular environment. Rather than relying solely on global mathematical equations or black-box predictions, ECR organizes biological processes into modules with explicitly defined responsibilities and execution sequences, enabling intracellular information processing and extracellular responses to progress continuously within a unified temporal framework.



ECR uses the Tick as its fundamental unit of temporal progression. Each Tick begins with the World state retained from the preceding Tick and follows a predefined execution sequence comprising environmental information acquisition, intracellular decision-making, and World state updates. First, ScanMaster retrieves interaction information between entities in the World, such as Cells and Fields, and performs preliminary filtering to generate candidate Events. InputBuilder then receives these Events, applies further filtering and processing, and converts the relevant information into numerical inputs that can be used by CellMaster. Next, CellMaster independently generates decisions for each Cell based on its currently recorded state, the Graph associated with its Cell Type, and the corresponding mechanistic JSON definitions. Its internal processing follows a predefined sequence of stages: Node → Passive → Gene → Behavior. Every Cell passes through this complete sequence, even when a particular stage requires no active operation during the current Tick. Different Cells and Graphs may nevertheless follow different execution paths and contain different mechanistic components. Once individual Cells have completed their decision-making processes, their resulting decisions are collectively submitted to IntentBuilder for aggregation and processing. IntentBuilder transforms these decisions, which have not yet been committed as actual state changes, into intents in a format accepted by LabelCenter. Finally, LabelCenter centrally executes persistent state updates and changes to entity existence, committing the resulting modifications to the World and completing the current Tick. The updated World state then serves as the starting state for the next Tick, forming a continuous cycle of interactions between the external environment and intracellular decision-making.



Within this architecture, Cell ID uniquely identifies each individual cell entity and supports the retrieval of its identity, spatial location, and associated records. Cell Type, in contrast, provides the type-specific information that guides intracellular decision-making in CellMaster, linking each Cell to its corresponding Graphs and mechanistic definitions. Unlike Cell ID, Cell Type is not an immutable identifier and may change during cellular development and state transitions.



The overall ECR architecture, the responsibilities of individual modules, and their execution mechanisms are described in the following sections, along with the architectural changes introduced across different versions. The current demo primarily operates with simulated inputs and predefined mechanistic configurations rather than experimentally derived biological datasets. Subsequent sections will outline the planned integration of real biological data, including the types of experimental measurements to be incorporated, how these data will be mapped to the corresponding ECR components, and how mechanistic equations and quantitative parameters are intended to support data-informed model construction and analysis.



###### 2\. world

The World is the two-dimensional spatial domain that serves as the environment and interaction space for ECR. It provides the spatial representation of biological entities and their associated data, primarily comprising Cells and Fields. Each entity is represented by its spatial coordinates and occupied area, allowing the World to describe the spatial distribution of cells and extracellular signals, as well as their potential spatial interactions. The coordinates of an entity refer to its center or relative center position, while its area represents the spatial extent it occupies rather than a fixed number of complete grid units. Cells and Fields are allowed to overlap spatially, enabling the representation of interactions between cells and their surrounding environments.



The World currently accommodates two primary entity types: Cells and Fields. Each Cell is associated with an ID, Type, Coordinate, Area, Node, Gene, and Label. The ID uniquely identifies an individual cell, while Type provides the classification information used to guide its intracellular decision-making processes. Coordinate and Area describe its spatial position and extent, whereas Node, Gene, and Label store its corresponding intracellular and cell-associated data. Each Field is associated with a Type, ID, Coordinate, Area, and Concentration. Fields represent extracellular signals or substances within the spatial environment, with their individual types distinguishing the corresponding substances or signals. Their coordinates and areas define their spatial distribution, while Concentration represents the associated concentration information. Each substance has its own corresponding Field, whose spatial extent can change through diffusion. Future spatial representations are intended to support irregular field geometries and spatially varying concentration distributions, rather than being restricted to uniform, regularly shaped regions.



Beyond serving as a spatial environment, the World is the sole source of persistent biological state and the authoritative representation of reality within ECR. All biological entities, their spatial relationships, and their persistent state information are maintained in the World. In contrast, Events, Decisions, and Intents are computational representations generated during runtime. They facilitate information acquisition, intracellular decision-making, and update coordination, respectively, but do not constitute independent biological entities or persistent changes to the World. Information is therefore retrieved from the World through the upstream processing modules and transformed into computational representations for subsequent processing. Once decisions have been aggregated and processed into Intents, LabelCenter executes the corresponding updates and commits the resulting changes to the World. These updates overwrite the relevant current state records, while historical states, when required, are intended to be maintained through separate recording mechanisms rather than by retaining successive historical snapshots within the World itself.



###### 3\. scanmaster

ScanMaster is responsible for scanning the World, identifying potential interactions between biological entities, and generating Events for subsequent processing by InputBuilder. It operates once per Tick and examines four types of entity interactions: Cell–Cell, Cell–Field, Field–Cell, and Field–Field. Rather than first generating an exhaustive list of all possible entity combinations and then filtering them, ScanMaster uses an independent Information Provider Library to guide the scanning process and identify potential information providers and their corresponding interaction candidates.



The Information Provider Library defines the entities or entity-associated components that can act as Information Providers, together with their corresponding triggering conditions. Both Cell Labels and Field Types can be registered as Information Providers. During scanning, ScanMaster uses these definitions to identify potential providers and examines whether their triggering conditions are satisfied in the context of other entities in the World. For example, Field concentration may contribute to the triggering process. However, the specific relationship between concentration and provider activation, including the possible use of concentration-dependent matching probabilities or other quantitative functions, remains subject to further biological investigation and model development.



Once a potential interaction satisfies the relevant provider conditions, ScanMaster organizes the corresponding information into an Event. An Event records the identity of the Information Provider, the identity of the other participating entity, and the associated interaction position. When either participant is a Field, its corresponding concentration information may also be included. The interaction position represents the location associated with the potential interaction rather than simply the center coordinate of either entity. Events are computational representations generated during runtime; they do not constitute independent biological entities or persistent changes to the World.



ScanMaster performs preliminary interaction screening based on Information Provider definitions and their triggering conditions. It does not determine whether the other participating entity possesses the appropriate recognition or response capability, nor does it execute the downstream biological response. These responsibilities belong to subsequent processing stages. The detailed quantitative rules for provider activation, spatial interaction positioning, and the handling of multiple or repeated candidate Events remain open for further development as additional biological knowledge and spatial modeling requirements are incorporated.



###### 4\. inputbuilder

InputBuilder is responsible for validating the candidate Events generated by ScanMaster, processing valid interactions, and transforming the resulting information into numerical inputs for CellMaster. While ScanMaster identifies potential information providers and generates candidate Events based on their triggering conditions, InputBuilder performs a second stage of screening to determine whether the corresponding information providers and receivers form valid interaction relationships.



InputBuilder maintains an independent Information Provider–Receiver Library, which defines the valid relationships between Information Providers and Information Receivers. Both Cell Labels and Field Types can serve as Information Receivers. For each Event received from ScanMaster, InputBuilder examines the identity of the Information Provider and the corresponding entity to determine whether an appropriate Information Receiver is present. Only Events whose provider–receiver combinations match the definitions in the Library are retained as valid interactions for subsequent processing. This validation step distinguishes potential interactions identified during scanning from interactions that can be meaningfully interpreted within the defined biological system.



Following validation, InputBuilder processes the information associated with each valid interaction and converts it into numerical representations that can be interpreted by CellMaster. This processing may involve connecting continuous Field information with discrete particle-level processes, a relationship referred to here as Field–Particle duality. For example, in a ligand–receptor interaction, Field concentration can be used to derive the corresponding ligand quantity within the relevant interaction context. The subsequent processing may account for ligand–receptor binding and the resulting changes in receptor states or polymorphic configurations. These processes are represented through quantitative calculations rather than direct modifications to the biological entities in the World.



The resulting information is organized into numerical inputs containing the target Cell's ID, Type, the corresponding Label or Receptor, and the associated Value. These inputs provide CellMaster with the information required for its intracellular decision-making processes, without requiring CellMaster to interpret the original external interaction data or reconstruct the intermediate calculations. Intermediate processing steps may also be retained as explanatory information for observation and analysis, while the numerical inputs constitute the actual information passed to CellMaster.



InputBuilder operates exclusively on information retrieved from the World and Events generated during runtime. It does not directly modify Cells, Fields, Labels, or any other persistent World state. Its role is to validate and translate external interaction information into a form suitable for intracellular processing. Persistent changes to biological entities are handled centrally by LabelCenter through the subsequent update process.



###### 5\. cellmaster

CellMaster is the central execution framework responsible for organizing intracellular computation for individual Cells within ECR. It acts as a shared computational framework rather than an independent biological mechanism or an autonomous decision-making entity. CellMaster itself does not generate biological responses without input; instead, it coordinates the processing of information received from InputBuilder and the current state of each Cell. Based on the Cell's Type, associated Graph, and corresponding mechanistic JSON definitions, CellMaster retrieves the required computational components and invokes the appropriate Engines to organize and execute the intracellular processing workflow.



All Cells use the same CellMaster framework, while their individual computations remain independent. Cells of the same Type may share Graph definitions, mechanistic configurations, and computational resources, but they retain their own inputs, internal states, and execution processes. Consequently, CellMaster does not require Cells of the same Type to be merged into a single computational process. Instead, it provides a common execution structure through which each Cell independently processes its own information according to its associated mechanisms and current conditions.



A defining feature of CellMaster is its layer-wise pre-execution planning. Although Graphs describe the relationships among Nodes, Genes, and Behaviors, the participation of individual components in a given Tick depends on the current inputs and cellular state. Determining all computational participants and their execution requirements in advance may therefore be insufficient when later stages depend on the results of earlier calculations. CellMaster addresses this by planning the computational tasks independently at each stage. After the completion of one stage, its results provide the basis for determining the potential participants and execution requirements of the next stage. This process continues throughout the intracellular workflow, allowing the computational plan to adapt to the conditions and results of the current Tick. Predefined network configurations may also be retained as reusable structural references, while the execution plan itself is generated independently for each Tick and is not inherited from previous Ticks.



Despite the dynamic planning of individual computational stages, the overall execution sequence remains fixed: Node → Passive → Gene → HIR → Behavior. Every Cell must pass through all five stages in this order, regardless of whether a particular stage contains active computational tasks during the current Tick. Within each stage, the corresponding planning process determines which components participate and how their calculations are organized, while the respective Engines execute the mechanisms defined by the associated JSON configurations. CellMaster coordinates these operations and collects the resulting intracellular decisions, which are subsequently passed to IntentBuilder for further processing. Through this architecture, CellMaster provides a unified but input-driven framework for organizing independent cell-level computation while preserving a consistent execution sequence across different Cell Types.



###### 5.1 scheduler

Scheduler is responsible for determining whether an individual Cell should initiate intracellular computation during the current Tick. It evaluates external inputs and the Cell's current internal state to identify Cells that require processing, and organizes the corresponding inputs before passing them to CellMaster. Scheduler does not perform Graph retrieval or determine the execution order of intracellular mechanisms. These responsibilities are handled by the Graph Engine and the corresponding computational components within CellMaster.



Cell activation can be triggered by external Events or by conditions arising from the Cell's own internal state. For external activation, Scheduler receives the valid Events generated by InputBuilder and organizes them according to their target Cell IDs. Since a Cell may receive multiple Events within the same Tick, Scheduler groups the Events belonging to the same Cell into a unified input collection. This ensures that each activated Cell enters CellMaster with its relevant external inputs organized together, rather than being scheduled repeatedly for individual Events.



In addition to external activation, Scheduler supports continued computation based on the Cell's internal state. One form of internal activation is forced continuous execution, which applies when a Cell enters a biological process that requires continued computational progression, such as apoptosis. Such conditions can be represented by specific Node values or corresponding Labels within the Cell. Scheduler examines these state indicators and their associated values to determine whether the Cell must continue executing, even in the absence of new external Events.



Another form of internal activation is state-dependent reactivation, which determines whether a Cell should continue processing a response initiated during a previous Tick. A Cell may undergo substantial internal changes following an external input, and these changes may require further computational progression even after the original input is no longer present. Scheduler can therefore evaluate changes in the Cell's internal state between consecutive Ticks to determine whether continued computation is necessary. This mechanism provides a means of identifying ongoing cellular responses without requiring every Cell to execute continuously or treating the persistence of individual molecular components, such as mRNA, as an independent activation condition.



When a Cell satisfies multiple activation conditions during the same Tick, Scheduler consolidates the relevant activation reasons and inputs into a single computational task for that Cell. Once the activation decision and input organization are complete, the selected Cells are passed to CellMaster for intracellular processing. Through this mechanism, Scheduler coordinates when individual Cells enter the computational workflow while allowing Cells without new inputs or ongoing internal processes to remain inactive during the current Tick.



###### 5.2 internalnet

InternalNet is the intracellular computational system invoked by CellMaster to organize and execute the internal decision-making processes of individual Cells. While CellMaster coordinates the overall cell-level computational workflow, it does not directly interact with the individual internal Engines. Instead, it delegates intracellular processing to InternalNet, which coordinates Graph retrieval, mechanism execution, and the generation of the corresponding computational results. InternalNet consists of multiple specialized Engines, each responsible for a distinct part of the intracellular processing workflow, while maintaining the prescribed execution sequence: Node → Passive → Gene → HIR → Behavior.



The Graph Engine provides the structural basis for intracellular computation. It retrieves the Graph configurations permitted for the current Cell Type and manages their use during execution, including the identification and planning of computational participants at each stage. The remaining Engines perform the corresponding calculations according to the mechanisms and parameters defined in their associated JSON configurations. Together, these components allow CellMaster to organize cell-specific decision-making based on the Cell's current inputs, internal state, Type, and associated Graph, without embedding individual biological mechanisms directly into the overarching execution framework.



Intracellular computation proceeds through a sequence of stages, with each stage operating on the results produced by the preceding stage. A continuous RuntimeState is maintained throughout this process. Each RuntimeState contains the numerical values and polymorphic states of both Nodes and Genes, including components that remain unchanged during a particular stage. Consequently, each Engine receives the complete RuntimeState from the previous stage, performs its designated calculations, and produces an updated RuntimeState for subsequent processing. This approach preserves the complete intracellular state throughout the computational workflow while allowing individual stages to modify only the components relevant to their respective mechanisms.



Within this workflow, the Node Engine integrates external numerical inputs with the previously recorded Node states and calculates the corresponding changes in Node polymorphism. The Passive Engine subsequently processes passive mechanisms, including molecular degradation through half-life and other state transitions. The Gene Engine handles Node–Gene regulatory relationships, particularly regulatory effects that modify or introduce Gene polymorphisms through changes associated with DNA or chromatin states. These stages establish the updated intracellular conditions that are subsequently used by HIR to organize behavioral decision-making.



HIR serves as a coordinating Engine within the intracellular decision-making process. It invokes the Behavior Engine to calculate behavioral intentions or tendencies, then organizes the subsequent parameter adjustments, including transcription factor (TF)-dependent adjustments and resource-dependent adjustments. TF adjustments apply specifically to transcription-related behaviors and affect only the current Tick, whereas resource adjustments account for the availability and allocation of cellular resources. By integrating behavioral intentions with these adjustments, HIR generates the resulting Behavior RuntimeState. The subsequent behavioral and cellular identity-related processing determines the corresponding outcomes, including resource utilization and changes in Cell Type, Lineage, and Label.



The resulting intracellular outputs are passed to StateUpdate for subsequent state updating. The Type, Lineage, and Label determinations are treated as current-Tick results that overwrite their corresponding records during the update process, rather than as direct modifications to the World during InternalNet execution. Through this architecture, InternalNet provides the computational mechanisms through which CellMaster organizes intracellular decision-making, integrating external information, internal state transitions, gene regulation, behavioral tendencies, and cell identity determination into a continuous and structured execution process.



###### 5.2.1 graph engine

The Graph Engine is responsible for retrieving, composing, and managing the Graph structures used in intracellular computation, as well as organizing pre-execution planning for individual processing stages. Based on the current Cell Type, it retrieves the corresponding Graph structures and combines the Housekeeping Graph, the Common Graphs associated with different levels of the Cell's Lineage, and the Type-specific Graph. These Graphs are assembled into the Graph collection available to the current Cell. According to the requirements of the calling component and the current processing stage, the Graph Engine further determines which types of Edges are permitted for use, providing the corresponding relationship structures for subsequent computation.



A Graph consists of four types of components: Nodes, Genes, Behaviors, and Edges. Edges describe biological relationships between computational components and currently include four types: Node–Node, Node–Gene, Node–Behavior, and Gene–Behavior. Each Edge belongs to a single Graph and contains information such as its name, relationship type, source, target, direction, and, where applicable, its associated relationship or formula category. Edges describe the relationships between components; they do not directly contain biological calculation formulas or define the complete execution sequence. The corresponding mechanisms and calculation formulas are provided by the associated JSON definitions.



Another major responsibility of the Graph Engine is pre-execution planning. Before formal computation begins, the Graph Engine uses the Graphs available to the current Cell and the Edge types permitted for the current processing stage to organize the potentially participating components and their associated paths. This process provides structural guidance for the subsequent execution of the corresponding Engines. It does not execute biological formulas or perform numerical calculations, but instead identifies the computational relationships that may be relevant during the current Tick based on the available Graph structure.



Pre-execution planning is performed independently for the different processing stages, including Node, Gene, and Behavior. The planning requirements differ across these stages. The Node stage primarily involves Node–Node relationships and requires the organization of local computational paths and execution order. Depending on the corresponding formula types, related calculations may be combined when necessary or performed sequentially when they do not require shared intermediate states. The Gene stage primarily involves Node–Gene relationships, where the regulatory effects of multiple transcription factors (TFs) on the same Gene are considered together. The Behavior stage uses Node–Behavior and Gene–Behavior relationships to identify the Behaviors that may participate in the current computation. Different Behaviors are independent of one another and can be calculated together within the same stage without requiring an execution dependency order between them.



Pre-execution planning provides guidance on potentially relevant computational components and paths rather than making the final determination of actual participants. Consequently, the relationships and components identified during planning may exceed those required for formal computation. The corresponding Engines still perform their calculations according to the current RuntimeState, the associated mechanistic definitions, and the actual computational conditions. For structurally stable and important local paths or execution patterns, the Graph Engine may also retain reusable pre-execution planning templates. However, the specific planning for each Tick is generated independently according to the current Cell Type, permitted Graph structures, and processing-stage requirements.



###### 5.2.2 node engine

The Node Engine is responsible for integrating external inputs with the current Node states of an individual Cell and performing the corresponding calculations at the Node stage. Following the activation decision made by Scheduler, it receives the consolidated Event inputs together with the Node and Gene values and polymorphic states recorded in the World. These records are integrated into the initial RuntimeState for the current computation. The Node Engine then uses the pre-execution planning provided by the Graph Engine and the Node–Node Edges permitted for the current Cell Type to identify and execute the corresponding mechanisms, determining changes in Node quantities and polymorphic states during the current Tick.



A Node is an abstract representation of substances that physically exist within a Cell and their associated states. It records not only the quantity of a substance but also its different possible states within the cellular environment. For example, an ATP Node may record the quantities of ATP and ADP; a PTCH1 Node may distinguish between active and inactive states; an SMO Node may distinguish between cholesterol-bound and unbound states; and a transcription factor (TF) Node may record its subcellular localization, such as whether it is located in the cytoplasm or the nucleus. These states are often mutually exclusive. Therefore, Node polymorphism requires explicit consideration of the priority and specificity of different states to avoid assigning the same substance to incompatible categories.



For example, GLI3 can be represented through polymorphic states that account for its SUFU-binding status, processing state, and subcellular localization. These include SUFU-bound, free, processed cytoplasmic, and processed nuclear states. Here, free refers to GLI3 that is not bound to SUFU and has not entered the corresponding processed states; processed cytoplasmic refers to GLI3 that has undergone processing in the cytoplasm but has not entered the nucleus; and processed nuclear refers to processed GLI3 located in the nucleus. To simplify model representation, not every substance, binding partner, or subcellular location needs to be represented explicitly as an independent Node. For example, unless required by a particular calculation or mechanism, SUFU may be represented indirectly through the SUFU-bound state of the GLI Node rather than as a separate Node.



The mechanistic calculations for Node–Node relationships are currently planned to cover two broad categories. The first involves direct molecular interactions or binding reactions, such as the interaction between retinoic acid (RA) and its receptor (RAR). These interactions generally have theoretical stoichiometric relationships, and their binding and dissociation kinetics can be measured through in vitro experiments. The model focuses on the amount of binding that occurs during the current Tick, rather than solely on the instantaneous binding rate. A general conceptual representation of the calculation is:



\\\[

\\Delta B\_{\\mathrm{Tick}}

=

\\int\_{t}^{t+\\Delta t}

\\left(

k\_{\\mathrm{on}}\[L]\[R]

\-

k\_{\\mathrm{off}}\[LR]

\\right)

\\,d\\tau

\\]



where (N\_{\\mathrm{upstream}}) represents the relevant upstream Node quantity, (R\_{\\mathrm{stoichiometric}}) represents the theoretical quantity relationship, and the remaining terms represent the binding and dissociation dynamics and any applicable adjustments for binding effectiveness or intracellular environmental influences. The specific mathematical formulation depends on the underlying reaction mechanism and the available experimental parameters. For example, when a mass-action kinetic model is appropriate, the net change in bound complexes during one Tick can be represented as:



\\frac{k\_{\\mathrm{cat}}\[E]\[S]}{K\_m+\[S]}

\\Delta t

]



where (\[E]) and (\[S]) represent the enzyme and substrate quantities or concentrations, respectively, (k\_{\\mathrm{cat}}) is the catalytic rate constant, and (K\_m) is the Michaelis constant. The specific formulation depends on the underlying reaction mechanism and the availability of experimental parameters.



The second category involves indirect regulatory relationships, such as the relationship between PTCH1 and SMO. For interactions that do not occur through direct physical binding between the two components, the model will instead seek to identify the variables necessary to describe their dynamic changes. The relevant variables, mathematical relationships, and quantitative coefficients will be determined according to the available experimental data and the biological mechanisms that these data can support. The specific formulation is therefore not predefined and will depend on the evidence obtained from the corresponding experimental systems.



After completing its calculations, the Node Engine updates the relevant Node quantities and polymorphic states in the current RuntimeState while retaining all unchanged Node and Gene information. It then produces a complete updated RuntimeState containing the numerical values and polymorphic states of both Nodes and Genes, and passes it directly to the subsequent Passive Engine. Each subsequent stage continues computation using the complete RuntimeState updated by the preceding stage, rather than retrieving the original records from the World again. This continuous state transfer allows changes generated across different intracellular stages to accumulate within the same Tick, with the resulting updates submitted through the subsequent state-updating process.



###### 5.2.3 passive engine

The Passive Engine handles physiological processes that occur without direct active control by the Cell, such as molecular degradation and diffusion. Unlike the Node Engine, which calculates relationships between Nodes through Graph-defined mechanisms, the Passive Engine operates independently of the Graph. It applies predefined passive mechanisms to the current cellular state whenever their corresponding conditions are met.



The Passive Engine receives the complete RuntimeState from the Node Engine, including the numerical values and polymorphic states of all Nodes and Genes. It scans these records and identifies the passive mechanisms applicable to each object according to their JSON definitions. These definitions specify the target objects, applicable conditions, formulas, and parameters required for each mechanism. Objects without applicable passive mechanisms retain their existing values and states.



Passive mechanisms are organized into a shared mechanism library and follow a global execution order across Cell Types and Lineages. Rather than defining separate passive processes for individual Cell Types, ECR treats these mechanisms as general physiological processes that may occur across different kinds of Cells. However, the applicability of each mechanism still depends on the properties and current states of the corresponding objects.



The mechanisms are executed sequentially. Each mechanism reads the current RuntimeState, performs its calculation, and updates the relevant numerical values or polymorphic states. Subsequent mechanisms then use the updated RuntimeState as their input. Consequently, the execution order determines which intermediate results are available to later mechanisms and is an explicit part of the computational design.



The parameters used by passive mechanisms are expected to be informed primarily by experimental measurements obtained in vitro, with additional consideration of intracellular environmental influences where applicable. The specific data sources and adjustment methods may differ between mechanisms. For example, degradation and diffusion require different physical and biochemical parameters, and their respective formulations should reflect the available experimental evidence.



After all applicable passive mechanisms have been executed, the Passive Engine outputs the complete updated RuntimeState, retaining both modified and unchanged Node and Gene information.



###### 5.2.4 gene engine

The Gene Engine is responsible for calculating changes in Gene states through transcription factor (TF)-mediated regulation. Unlike the Node Engine, which handles Node–Node relationships, the Gene Engine uses Node–Gene relationships to describe how TFs regulate specific Genes through their corresponding regulatory elements. These interactions can modify the intrinsic regulatory states of Genes, and the resulting changes are retained in subsequent Ticks.



A Gene is represented by its numerical values and polymorphic states, which collectively quantify its current transcriptional competence. These states can be described using biological and experimental representations of gene regulation, including DNA accessibility, chromatin accessibility, nucleosome occupancy and positioning, histone modifications, DNA methylation, and other relevant chromatin states. For example, histone modifications such as H3K27ac, H3K4me3, H3K27me3, and H3K9me3 can be used to represent different aspects of the regulatory state of a Gene. These properties are not necessarily mutually exclusive; multiple state dimensions and their corresponding numerical values can coexist within the same Gene. The specific representations used depend on the available biological evidence and the requirements of the corresponding mechanisms.



The Gene Engine receives the complete RuntimeState from the Passive Engine and uses the pre-execution planning provided by the Graph Engine, together with the Node–Gene Edges permitted for the current Cell Type, to organize its calculations. For each regulatory relationship, the relevant TF quantity and polymorphic state are considered. In particular, the quantity of TF available for nuclear regulation is used where applicable, rather than the total quantity of the TF regardless of its subcellular localization.



The calculation considers several contributing factors: the current numerical values and polymorphic states of the target Gene, the available quantity and state of the corresponding TF, the binding and dissociation dynamics between the TF and its regulatory Element during the current Tick, the effectiveness of the binding where applicable, and the regulatory effect of the specific TF–Gene combination. These relationships can be conceptually represented as:



f\\left(

G\_{\\mathrm{current}},

TF,

B\_{\\mathrm{TF-Element}},

E\_{\\mathrm{binding}},

E\_{\\mathrm{TF-Gene}}

\\right)

$$



Here, $G\_{\\mathrm{current}}$ represents the current Gene state, $TF$ represents the relevant TF quantity and polymorphic state, $B\_{\\mathrm{TF-Element}}$ represents the binding state or binding change during the current Tick, $E\_{\\mathrm{binding}}$ represents binding effectiveness where applicable, and $E\_{\\mathrm{TF-Gene}}$ represents the regulatory effect of the specific TF–Gene combination. The function $f$ describes the overall relationship among these contributing factors; it does not prescribe a universal mathematical formula.



The TF–Gene regulatory effect represents the combined effect of a specific TF on a specific Gene. At the current stage, this effect may need to be estimated from available biological knowledge and experimental observations, as it may not be directly measurable with existing data. Where experimentally determined effects become available, these measurements can be used directly instead of relying on estimation. The specific mathematical formulation and parameters depend on the corresponding regulatory mechanism and the available evidence.



When multiple TFs regulate the same Gene, their effects are generally calculated sequentially, with each subsequent calculation using the Gene state updated by the preceding calculation. This allows individual regulatory contributions to accumulate without requiring all TFs to be calculated together. However, when multiple regulatory relationships cannot be treated independently, such as in cases involving coupled regulatory effects, the relevant factors are calculated together. The pre-execution planning provided by the Graph Engine helps identify the relationships that require coordinated calculation.



After completing its calculations, the Gene Engine updates the relevant Gene numerical values and polymorphic states while retaining all unchanged information. These changes represent persistent modifications to the Gene's regulatory state and are carried forward into subsequent Ticks. The Gene Engine does not directly execute transcription or translation; these processes are handled by the Behavior Engine. Likewise, direct TF-mediated adjustments to transcription-related Behavior parameters belong to the HIR layer rather than the Gene Engine.



The Gene Engine outputs the complete updated RuntimeState, including all Node and Gene numerical values and polymorphic states, and passes it to HIR for the next stage of intracellular computation.



###### 5.2.5 hir

HIR (Hierarchical Integration and Regulation) is the coordinating component of InternalNet. It integrates behavior intention calculations, parameter adjustments, and cell identity-related determinations into a unified execution process.



HIR does not independently define the biological mechanisms of each Behavior. Instead, it coordinates the relevant Engines and applies the mechanisms and parameters specified in their corresponding JSON configurations.



HIR operates on the complete RuntimeState passed from the Gene Engine, together with the pre-execution plan and the Graph relationships authorized for the current Cell Type. It uses Node–Behavior and Gene–Behavior Edges to identify the relationships relevant to behavior-related calculations.



HIR consists of three main parts:



Behavior intention calculation



Parameter adjustment



Type / Lineage / Label determination



Behavior Intention Calculation



HIR invokes the Behavior Engine to calculate the theoretical quantity of each Behavior based on the current RuntimeState.



The Behavior Engine uses Node–Behavior and Gene–Behavior relationships, together with their corresponding JSON-defined mechanisms, to determine how the current molecular and gene states contribute to each Behavior.



The resulting values represent behavior intentions: the theoretical quantities that could be produced under the current cellular conditions, before resource constraints are applied.



The detailed calculation mechanisms are described in 5.2.6 Behavior Engine.



Parameter Adjustment



After behavior intentions have been calculated, HIR adjusts them according to transcription-related regulatory effects and resource availability.



TF Adjustment



TF adjustment provides an additional, current-Tick regulation of transcription-related Behaviors. It considers relevant TF quantities and polymorphic states, TF–Element binding states, binding effectiveness where applicable, and the specific TF–Gene regulatory effect.



The adjustment can be conceptually represented as:



f(I\_{\\mathrm{transcription}}, TF, B\_{\\mathrm{TF-Element}}, E\_{\\mathrm{binding}}, E\_{\\mathrm{TF-Gene}})

$$



This adjustment affects the current transcription Behavior intention. It does not directly modify the Gene's numerical values or polymorphic states, and is not retained as a persistent Gene-state change.



This is distinct from the Gene Engine, where TF-related regulation can produce persistent changes in the Gene's transcriptional state.



Resource Adjustment



Resource adjustment determines the actual executable quantity of each Behavior under the resource constraints of the current Tick.



The process follows three steps:



Calculate resource capacity. Determine the total available capacity of each relevant resource based on its current quantity, consumption requirements, occupancy capacity, and other applicable constraints.



Allocate resources among Behaviors. Distribute available resources among the Behaviors that require them, accounting for competition between different Behaviors.



Determine actual Behavior quantities. Within each Behavior, determine the actual executable quantity according to its adjusted intention and allocated resources.



A Behavior may require multiple resources simultaneously. Its actual executable quantity is therefore constrained by the availability of all required resources. For example, protein production may depend on amino acids and ATP as consumable resources, as well as ribosome availability as an occupancy constraint.



Resources can be broadly distinguished into:



Consumable resources, such as ATP, amino acids, nucleotides, lipids, and glycerol. Their quantities can be affected by Behavior execution.



Occupancy resources, such as ribosomes and enzymes, which constrain the capacity for simultaneous or ongoing execution. Occupancy is represented as a temporary allocation record rather than automatically treated as resource consumption or a persistent change in resource quantity.



The result of resource adjustment is the actual numerical output of each Behavior, distinguishing it from the theoretical quantity calculated during behavior intention determination.



Type / Lineage / Label Determination



HIR also coordinates Type, Lineage, and Label determination using the Behavior RuntimeState.



This part does not constitute another numerical behavior calculation. It is an additional determination and update process associated with the current cellular state. Its detailed structure and rules are described separately in 5.2.7 Type / Lineage / Label.



Output



HIR produces the Behavior RuntimeState, which contains the actual numerical results of Behavior execution and the relevant information required by subsequent processing.



Behavior outputs are numerical values, generally expressed as quantities of substances or, where appropriate, other physical units such as distance. HIR does not determine how these values are applied to the World. Their interpretation and application—for example, updating intracellular quantities, producing extracellular Field quantities, or representing movement—are handled by LabelCenter.



HIR does not directly modify the World. Its results are passed to subsequent components for further processing.



###### 5.2.6 behavior engine

The Behavior Engine calculates the theoretical quantities of cellular Behaviors based on the current RuntimeState. It is invoked and coordinated by HIR as part of the behavior intention calculation process.



The Behavior Engine does not directly execute biological processes, consume resources, modify the World, or determine how its numerical outputs are applied. Its responsibility is to translate the current molecular and gene states into numerical behavior intentions using the mechanisms and parameters defined in JSON configurations.



Inputs and Regulatory Relationships



The Behavior Engine receives the complete RuntimeState passed through the preceding stages, including Node and Gene numerical values and polymorphic states.



It uses the Graph Engine's pre-execution plan and the Node–Behavior and Gene–Behavior Edges authorized for the current Cell Type to identify the regulatory relationships relevant to each Behavior.



The two Edge types represent different sources of behavior regulation:



Node–Behavior: Describes how the current quantity or state of a Node contributes to a Behavior.



Gene–Behavior: Describes how the transcriptional competence represented by a Gene contributes to a transcription-related Behavior.



The corresponding formulas and parameters are defined in JSON mechanisms rather than stored directly in the Edges.



Node–Behavior Relationships



Node–Behavior relationships describe how molecular quantities or states contribute to the theoretical quantity of a Behavior.



Node values often represent measurable physical quantities, such as the amount or concentration of a molecule. These values can be translated into behavior-related quantities through mechanism-specific formulas, conversion factors, or proportional relationships.



For example, the amount of mRNA may contribute to the theoretical quantity of protein production during a Tick. A mechanism could relate the available mRNA quantity to its theoretical protein production capacity over the relevant time interval.



The resulting Behavior intention is expressed as a numerical quantity with an appropriate unit. For material production or consumption, this will generally be an amount of substance. Other types of Behaviors may use other appropriate physical units, such as distance.



The specific mathematical relationship depends on the biological mechanism and its corresponding JSON definition. No single conversion formula is imposed on all Node–Behavior relationships.



Gene–Behavior Relationships



Gene–Behavior relationships describe how the transcriptional competence represented by a Gene contributes to a transcription-related Behavior.



A Gene's numerical values and polymorphic states represent its current transcriptional competence. However, these dimensions do not necessarily translate directly or linearly into transcriptional output.



The Behavior Engine therefore uses the corresponding JSON-defined mechanism to integrate the relevant Gene-state dimensions and determine their effective contribution to the transcription Behavior intention.



Different Gene-state dimensions may interact conditionally or nonlinearly. For example, the contribution of one chromatin feature may depend on the presence or state of another feature. These relationships are defined by the mechanism associated with the relevant Gene–Behavior relationship.



The resulting value represents the theoretical quantity of transcription-related Behavior under the current Gene state. It does not represent an actual transcription event or directly update mRNA quantity.



Behavior Intention Output



For each Behavior, the Behavior Engine produces a numerical intention representing its theoretical quantity under the current cellular conditions.



These values are passed to HIR for subsequent parameter adjustment and resource allocation. The resulting actual executable quantities are determined by HIR, taking into account regulatory adjustments and resource constraints.



All Behavior outputs are numerical. Their units depend on the nature of the represented quantity, rather than being converted into a universal abstract action score.



The Behavior Engine does not determine the destination or application of these values. Whether a numerical result updates an intracellular quantity, contributes to an extracellular Field, or represents a spatial change is determined downstream by LabelCenter.



###### 5.2.7 type lineage

Type, Lineage, and Label are determined and updated within HIR after resource adjustment has produced the Behavior RuntimeState. They represent an additional state-determination process rather than another stage of numerical behavior calculation.



These components serve different purposes:



Type identifies the Cell's current developmental position and its remaining or potential capabilities.



Lineage provides the fixed developmental hierarchy within which Type is determined.



Graph authorization connects the current Type to the biological relationships that InternalNet is permitted to use.



Label provides an externally accessible representation of selected cellular properties.



Type Determination

Type is a dynamic determination made at every Tick based on the current Behavior RuntimeState and the developmental relationships defined by Lineage.



The determination considers the biological progression of cellular states rather than simply checking whether individual Nodes are present. Developmental progression follows biologically meaningful prerequisites: for example, a specialized Gene cannot be activated without the required transcription factors, and a specialized transcription factor cannot become active without the necessary upstream receptor-related conditions.



Type determination therefore evaluates the current cellular state in the context of the required progression and its intermediate conditions.



A Type record contains three main categories of information:



Main Type: The Cell's current primary identity and developmental position.



Residual: Capabilities or mechanisms retained from previous developmental stages.



Potential: The possible downstream developmental directions that remain available to the Cell.



A Cell may retain multiple developmental potentials at the same time. When multiple potentials exist, their relative proportions can be represented as differentiation tendency probabilities derived from Type determination.



These probabilities are descriptive information intended to communicate the Cell's current developmental tendencies. They do not participate in numerical Runtime calculations, resource allocation, Behavior calculations, or Graph authorization.



Type is reassessed at every Tick, and the newly determined result overwrites the previous Type record. Developmental progression can move forward or, under sufficiently restrictive conditions, return to an earlier position in the Lineage structure. Reversal is not triggered by arbitrary fluctuations; it must satisfy the relevant biological progression criteria.



Lineage Structure

Lineage is represented by a single, fixed developmental tree shared by Cells within the ECR model.



The tree defines the relationships between developmental positions and their possible differentiation paths. It is a structural reference rather than a dynamic state that is regenerated as individual Cells change their identities.



Type determines a Cell's current position within this fixed tree. When Type changes, the Cell's position changes, but the Lineage structure itself remains unchanged.



The tree does not require all branches to split at the same developmental depth or to have equivalent numbers of stages. Two differentiation paths may diverge from an early shared developmental position when their biological progression begins to differ. Other paths may continue through shared stages before becoming more specifically separated.



This structure allows differentiation paths to have different branching positions and progression lengths while remaining part of the same Lineage tree.



Graph Authorization and Developmental Potential

Graph authorization connects the Cell's current Type to the Graphs available for InternalNet execution.



The Graphs themselves are defined and managed by the Graph Engine, as described in 5.2.1 Graph Engine. They include:



Housekeeping Graphs: Shared mechanisms representing basic cellular functions.



Common Graphs: Mechanisms shared across Cells at different levels of developmental Lineage.



Type-specific Graphs: Mechanisms associated with a particular Cell Type.



The Graph composition for a Cell is determined according to its current Type and the corresponding developmental context.



Graph authorization determines which biological relationships, represented by Edges, are permitted for use during InternalNet calculations. An Engine can only execute a mechanism through the relevant authorized relationships. The presence of a biological relationship in an unauthorized Graph does not make it available for the current Cell's computation.



Developmental progression is therefore associated with changes in the available Graph composition. As a Cell advances along a differentiation path, its authorized Graphs can become more specific, reflecting the mechanisms available at that stage. The developmental structure can also accommodate the gradual restriction of alternative differentiation capabilities.



The Main Type and its associated Graph authorization determine the Graphs used for the current Tick. Developmental potential describes possible future directions, but its associated differentiation tendency probabilities do not directly grant computational authorization.



Because Type determination occurs after the current Tick's numerical calculations, the newly determined Type and its Graph authorization are used in subsequent Ticks rather than retroactively changing the calculations already completed.



Label Determination

Label provides an externally accessible representation of selected cellular properties, corresponding to membrane proteins and their numerical states.



Label is determined and updated independently of Type. Its numerical values are derived from the corresponding Node values rather than maintained as an unrelated set of protein quantities.



External modules do not directly access the Cell's internal Node and Gene values or their polymorphic states. Instead, they use Label as the interface for identifying and interacting with Cells.



For example:



ScanMaster uses Labels to identify cellular interaction characteristics.



InputBuilder uses Labels when determining whether a Cell satisfies the relevant Receiver conditions.



Scheduler can use Labels as part of its internal activation conditions.



Label therefore provides a defined boundary between the Cell's internal computational state and the information exposed to external components.



Update and Tick Transition

After resource adjustment, HIR obtains the Behavior RuntimeState containing the final numerical results of the current Tick, together with the complete Node and Gene values and their polymorphic states.



HIR then independently determines and updates Type and Label:



Type is reassessed against the fixed Lineage structure and the biological progression criteria.



Label is updated from the corresponding Node values.



The newly determined Type replaces the previous Type and provides the basis for Graph authorization in the next Tick.



The Lineage tree remains fixed throughout these updates. The resulting Type and Label records are carried forward as part of the Cell's updated state, while the numerical Behavior outputs remain available for subsequent processing by downstream components.



###### 5.3 stateupdate

StateUpdate collects the outputs produced by CellMaster and packages them into Intent Requests for IntentBuilder.



Its primary responsibility is to ensure that the results generated by each Cell are correctly matched to their corresponding Cell IDs and transferred without losing their associated information.



Inputs

StateUpdate receives the following outputs from CellMaster:

Behavior RuntimeState: The final numerical state produced during the current Tick, including complete Node and Gene values and their polymorphic states.

Special Behaviors: The types and numerical values of special Behaviors, such as cellular actions or movement-related outputs.

Released Materials: The identities and numerical quantities of materials designated for release outside the Cell.

Type: The Cell's newly determined Type

Label: The Cell's updated external interface information.



Collection and ID Matching

StateUpdate organizes the received outputs by Cell ID. All information belonging to the same Cell is collected together, ensuring that its RuntimeState, Behavior outputs, Type, and Label remain correctly associated.

This ID-based organization preserves the identity and completeness of each Cell's output during the transfer to IntentBuilder.

StateUpdate does not interpret the biological meaning of Behavior outputs or determine their eventual effects. It records and packages the information provided by CellMaster without introducing additional biological decisions or numerical calculations.



Intent Request Packaging

After collection and ID matching, StateUpdate packages the results into Intent Requests and passes them to IntentBuilder.

Each request retains the corresponding Cell ID and its associated output information. The packaging process is intentionally lightweight: StateUpdate focuses on maintaining correct data associations and preserving the received results, rather than classifying or restructuring them according to their eventual effects on the World.

IntentBuilder is responsible for subsequent organization and formatting of the received requests into the appropriate update intents.

StateUpdate therefore serves as the output-side counterpart to InputBuilder: InputBuilder organizes external inputs for CellMaster, whereas StateUpdate collects and organizes CellMaster's outputs for IntentBuilder.



###### 6\. intentbuilder



IntentBuilder collects and integrates Requests generated by different ECR components and organizes them into a unified representation called Formal Intent.

It serves as the transition between computational outputs and their eventual application to the World. Its responsibility is to organize what needs to be updated, rather than determine the biological validity or directly execute the requested changes.



Request Collection

IntentBuilder receives Requests from different components, including the Intent Requests packaged by StateUpdate.

These Requests may concern different types of updates, such as:

Changes to intracellular numerical states.

Special Behavior outputs, including movement-related quantities.

Material release and other extracellular changes.

Cell Type and Label updates.

Other requests generated by ECR components.

Each Request retains its relevant entity identifiers, such as Cell IDs or Field IDs, so that the intended targets remain identifiable throughout subsequent processing.



Request Integration

IntentBuilder organizes and integrates the received Requests according to their content and intended update categories.

Requests associated with the same target or related updates can be collected and reorganized into a consistent representation. This process may involve classification, association, and formatting, while preserving the original target identities and numerical information.

IntentBuilder does not independently interpret biological mechanisms, determine whether a requested state transition is biologically valid, or modify persistent World states.



Formal Intent Generation

After integration, IntentBuilder produces Formal Intents and passes them to LabelCenter.

Formal Intent provides a unified representation of the requested updates, allowing LabelCenter to interpret, validate, and apply them using the relevant Libraries and state-management rules.

IntentBuilder therefore acts as the request integration and formalization layer between ECR's computational components and LabelCenter.



###### 7\. labelcenter

LabelCenter is the unified management center and Single Source of Truth (SSOT) for persistent Cell states and Labels in ECR. It receives Formal Intents from IntentBuilder, consults the relevant Libraries, resolves the requested changes, and applies the resulting updates to the World.

Unlike IntentBuilder, which organizes Requests into Formal Intents, LabelCenter is responsible for determining how these requests are validly implemented and ensuring that persistent states remain consistent.



Definition Lookup and Validation

LabelCenter consults the relevant Libraries to retrieve the definitions required to resolve Formal Intents.

These definitions may include:

Cell state and Label definitions.

Receptor presentation definitions.

Cell Type and Graph authorization relationships.

Material and Field-related definitions.

Cell creation templates.

LabelCenter uses these definitions to interpret and validate the requested changes before applying them.



Cell State and Label Management

LabelCenter centrally manages persistent Cell states and Labels.

Its responsibilities include:

Updating intracellular Node values and polymorphic states.

Managing Cell Labels and their numerical values.

Managing receptor presentation.

Applying Cell Type changes.

Updating the Graph authorization associated with the current Type.

A Type change modifies the Cell's Type and consequently its authorized Graph composition. It does not reconstruct or reinitialize the Cell's existing Node, Gene, or Behavior states. Graphs define the biological relationships available for InternalNet calculations; they do not store the Cell's actual numerical or polymorphic states.

LabelCenter also maintains the relationship between externally accessible Labels and their corresponding cellular properties.



Field–Particle Duality and World Updates

LabelCenter resolves the application of numerical results to the World, including the relationship between extracellular Field quantities and intracellular material quantities.

For example:

Material uptake can be applied as a corresponding increase in intracellular quantities and a decrease in extracellular Field quantities.

Material release can be applied as a corresponding decrease in intracellular quantities and an increase in extracellular Field quantities.

Movement-related outputs can be applied to update Cell spatial positions.

Other Behavior outputs can be translated into their corresponding Cell or Field state changes.

The specific application depends on the Formal Intent and the relevant definitions in the Libraries.

LabelCenter is the sole component responsible for writing persistent updates to the World. Other components provide calculations and Requests, but do not directly modify persistent World states.



Cell Factory

Cell Factory provides the templates used to create new Cells.

Under ordinary creation conditions, LabelCenter only needs to provide the essential creation information:

Coordinate: The new Cell's position in the World.

Cell ID: The unique identifier assigned to the new Cell.

Type: The initial Cell Type.

Cell Factory uses the specified Type to retrieve the corresponding Cell template and construct the new Cell with its predefined initial structure.

Additional creation parameters may be supplied when special requirements exist, but they are not necessary for ordinary Cell creation.

Cell Factory is therefore a creation mechanism, not a mechanism for reconstructing existing Cells when their Types change.



Final World Update

After resolving Formal Intents and retrieving the necessary definitions, LabelCenter applies the corresponding changes to the World.

These changes may include updates to existing Cell states, Labels, receptor presentation, Cell Types, Graph authorization, Field quantities, spatial positions, and the creation of new Cells through Cell Factory.

LabelCenter completes the transition from requested updates to persistent World changes, ensuring that the World remains the authoritative source of the current state of the ECR system.



###### 8\. demo

###### 9\. question

###### 

##### DA

###### 1\. overview

###### 2\. design

###### 3\. data

